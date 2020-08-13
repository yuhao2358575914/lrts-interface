import math
from decimal import Decimal
from time import sleep

from login.templates.admin.platform.common.operate_mysql import billing_select
from login.templates.admin.platform.settlement.get_CurrentTime import month_days, getCurrentTime


class SettlementVIP():
    '''VIP会员结算'''
    def __init__(self,settlement_month,entity_id,partner_id,book_days_rate):
        self.settlement_month=settlement_month
        self.entity_id=entity_id
        self.partner_id=partner_id
        self.book_days_rate=Decimal(str(book_days_rate))
    def adjustPercent_sql_record(self):
        '''计算可调节收入百分比涉及到的sql
        :param date 日期，如'202006'
        '''
        # 某个月VIP会员结算记录
        date_style = str(self.settlement_month)
        year_month = date_style[0:4] + '-' + date_style[4:6]
        # 结算开始时间
        start_time = year_month + '-01'+' 0:00:00'
        print(start_time)
        # 根据传入的结算月份得到结算结束时间
        days = month_days(date_style)
        end_time = year_month + '-' + str(days)+' 23:59:59'
        print(end_time)

        # base_billing_amount = billing_select("SELECT * FROM p_billing_records pbr where partner_id =1459 and sp_type=6 and billing_month='2020-06-01';","billing")
        #查询会员总净收入记录
        base_billing_amount=billing_select("SELECT sum(base_billing_amount) from p_member_order_item pmoi where start_time BETWEEN '%s' and '%s' and status=0 and base_billing_amount>0;"%(start_time,end_time),'billing')
        # 某个月所有等级的记录
        grade_record = billing_select('''SELECT a.*,grade.award_multiple,grade.need_reward from (
                                      SELECT (SELECT grade_id from p_member_grade_book pmgb where entity_id = pmpm.entity_id and product_type = pmpm.product_type and status=1) as grade_id,SUM(pmpm.play_count ) from p_member_play_month pmpm where 
                                      `month` = %s and status=0
                                      GROUP BY grade_id ) a left JOIN p_member_grade grade on id = a.grade_id ;'''%(self.settlement_month),"billing")
        # 某个月参与奖励的等级记录
        award_grade_record = billing_select('''SELECT a.*,grade.award_multiple,grade.need_reward from (
                                                    SELECT (SELECT grade_id from p_member_grade_book pmgb where entity_id = pmpm.entity_id and product_type = pmpm.product_type and status=1 ) as grade_id,SUM(pmpm.play_count ) from p_member_play_month pmpm where 
                                                    `month` = %s and status=0
                                                    GROUP BY grade_id ) a left JOIN p_member_grade grade on id = a.grade_id where grade.need_reward=1;'''%(self.settlement_month),"billing")
        # 某个月总有效播放次数记录
        all_play_count = billing_select("SELECT `month`,sum(play_count) from p_member_play_month where `status`=0 and `month` =%s;"%(self.settlement_month), "billing")
        return [base_billing_amount,award_grade_record,grade_record,all_play_count]
    def adjust_percent(self):
        '''可调节百分比
        :param 结算月份，如2020-06-01
        '''
        sql_record=self.adjustPercent_sql_record()
        base_billing_amount=sql_record[0][0]['sum(base_billing_amount)'] #会员总净收入
        print('会员总净收入：'+str(base_billing_amount))
        grade_record=sql_record[2] #某个月所有等级的记录
        award_grade_record=sql_record[1] #某个月参与奖励的等级记录
        all_play_count=sql_record[3][0]['sum(play_count)'] #某个月总有效播放次数
        playCount_multiple=0
        for every1 in grade_record:
            playCount_multiple+=every1['SUM(pmpm.play_count )']*Decimal(every1['award_multiple'])
        award_playCount_multiple=0
        award_playCount=0
        for every2 in award_grade_record:
            award_playCount_multiple+=every2['SUM(pmpm.play_count )']*Decimal(every2['award_multiple'])
            award_playCount+=every2['SUM(pmpm.play_count )']

        #需参与奖励的等级调节后的金额
        award_grade_adjust_amount=base_billing_amount/playCount_multiple*award_playCount_multiple
        print('需参与奖励的等级调节后的金额 '+str(award_grade_adjust_amount))
        print(type(award_grade_adjust_amount))
        #需参与奖励的等级实际金额
        award_grade_true_amount=base_billing_amount/all_play_count*award_playCount
        print('需参与奖励的等级实际金额'+str(award_grade_true_amount))
        print(type(award_grade_true_amount))
        #可调节金额
        adjust_amount=award_grade_adjust_amount-award_grade_true_amount
        print('可调节金额'+str(adjust_amount))
        #可调节净收入百分比
        adjust_percent_original=adjust_amount/base_billing_amount*100
        adjust_percent=math.floor(adjust_amount/base_billing_amount*100)
        print('可调节净收入百分比(原始值)'+str(adjust_percent_original))
        print('可调节净收入百分比：'+str(adjust_percent)+'%')


    def settlementAmount_sql_record(self,product_type):
        '''计算结算VIP会员结算金额涉及到的sql'''
        date_style = str(self.settlement_month)
        year_month = date_style[0:4] + '-' + date_style[4:6]
        # 结算开始时间
        start_time = year_month + '-01'+' 0:00:00'
        print(start_time)
        # 根据传入的结算月份得到结算结束时间
        days = month_days(date_style)
        end_time = year_month + '-' + str(days)+' 23:59:59'
        print(end_time)
        #查询书籍当月的有效播放次数记录
        book_playCount_record=billing_select("select * from p_member_play_month pmpm where entity_id=%s and product_type=%s and `month`='%s'  and status=0"
                                          %(self.entity_id,product_type,self.settlement_month),"billing")
        if book_playCount_record:
            book_playCount=book_playCount_record[0]['play_count']
        else:
            book_playCount=0
            print('当前结算月份该资源播放记录为空！！！')
        #查询书籍所在等级的奖励倍数
        award_multiple_record=billing_select('''select award_multiple from p_member_grade pmg where grade_type = 1 and id in (select grade_id from p_member_grade_book pmgb where entity_id=%s and product_type=%s and status=1)'''
                                            %(self.entity_id,product_type),"billing")
        award_multiple=award_multiple_record[0]['award_multiple']
        # 查询书籍所在等级的当月有效播放次数记录
        grade_id_record = billing_select("select grade_id from p_member_grade_book pmgb where entity_id=%s and product_type=%s and status=1;" % (self.entity_id, product_type), 'billing')
        grade_id = grade_id_record[0]['grade_id']
        grade_playCount_record = billing_select('''SELECT `month`,sum(play_count) from p_member_play_month where `month`='%s'  and product_type=%s and entity_id in 
                                                (SELECT entity_id from p_member_grade_book where grade_id=%s 
                                                 and `status`=1); '''
                                                % (self.settlement_month, product_type, grade_id), 'billing')
        grade_playCount=grade_playCount_record[0]['sum(play_count)']
        # 查询书籍所在等级的公司补贴级别系数记录
        reward_factor_record = billing_select('''select reward_factor from p_member_grade pmg where grade_type = 2 and id in (select company_subsidy_grade_id from p_member_grade_book pmgb where entity_id=%s and product_type=%s and status=1)'''
                                    % (self.entity_id, product_type), "billing")
        reward_factor=reward_factor_record[0]['reward_factor']

        # 查询会员总净收入记录
        platform_base_billing_amount_record = billing_select("SELECT product_type,sum(base_billing_amount) from p_member_order_item pmoi where start_time BETWEEN '%s' and '%s' and product_type=%s and status=0 and base_billing_amount>0;"
                                             % (start_time, end_time,product_type), 'billing')
        platform_base_billing_amount=platform_base_billing_amount_record[0]['sum(base_billing_amount)']
        print('会员总净收入:',platform_base_billing_amount)
        #查询某个平台的所有等级的播放次数和等级奖励倍数记录
        platform_playCount_awardMultiple=billing_select('''SELECT a.*,grade.award_multiple,grade.need_reward from (
                                                        SELECT product_type,(SELECT grade_id from p_member_grade_book pmgb where entity_id = pmpm.entity_id and product_type = pmpm.product_type and status=1) as grade_id,SUM(pmpm.play_count ) from p_member_play_month pmpm 
                                                        where `month` = '%s' and status=0 and product_type=%s
                                                        GROUP BY grade_id 
                                                        ) a left JOIN p_member_grade grade on id = a.grade_id ;'''%(self.settlement_month,product_type,),'billing')
        # 查询合作方的VIP合作业务
        partner_records = billing_select("SELECT * from p_partner_service where partner_id='%s' and service_type=6 ORDER BY id desc LIMIT 1" % (self.partner_id), "billing")
        if partner_records:
            partner_record=partner_records
        else:
            partner_record=0
        #查询主播合作方VIP分成资源记录
        Anch_partner_record = billing_select("select * from p_share_fee_resource where res_id = '%s' and share_fee_type = 3 order by create_time desc limit 1;"
                                            % (self.entity_id), "billing")
        #公司补贴百分比
        company_subsidy_percent_record=billing_select("select * from p_config_server pcs where config_key ='COMPANY_SUBSIDY_PERCENT';",'billing')
        company_subsidy_percent=company_subsidy_percent_record[0]['config_value']
        return [book_playCount,award_multiple,grade_playCount,platform_base_billing_amount,platform_playCount_awardMultiple,partner_record,Anch_partner_record,company_subsidy_percent,reward_factor]

    def platform_book_settlement_amount(self,product_type=1):
        '''版权/主播合作方结算计算
        :param product_type 平台
        '''
        # 合作方当月分成天数/当月总天数(分成天数占比）
        book_days_rate = self.book_days_rate
        #打印合作方id和资源id
        print('合作方id:' + str(self.partner_id) + '|' + '资源id:' + str(self.entity_id))
        #获取VIP会员业务结算涉及到的sql记录
        settlementAmount_sql_record=self.settlementAmount_sql_record(product_type)
        #书籍当月的有效播放次数
        if settlementAmount_sql_record[0]:
            book_playCount=settlementAmount_sql_record[0]
            print('书籍当月有效播放次数：'+str(book_playCount))
        else:
            book_playCount = 0
            book_platform_amount = 0
            book_platform_amount_final = 0
            print('书籍当月有效播放次数：' + str(book_playCount))
            print('书籍每月会员收入：' + str(book_platform_amount))
            print('书籍每月分成基数/本月可分成流水：' + str(book_platform_amount_final))
        # 书籍所在等级的有效播放次数
        grade_playCount = settlementAmount_sql_record[2]
        print('等级播放次数:',grade_playCount)
        print('等级播放次数:', type(grade_playCount))
        #书籍所在等级的奖励倍数
        award_multiple=Decimal(str(settlementAmount_sql_record[1]))
        # 平台会员总净收入
        platform_base_billing_amount = settlementAmount_sql_record[3]
        if grade_playCount and award_multiple:
            # 书籍所在等级放大后的有效播放次数
            grade_amplify_playCount = grade_playCount * award_multiple
            print('书籍所在等级放大后的有效播放次数:' + str(grade_amplify_playCount))
        else:
            grade_playCount=0
            grade_amplify_playCount=0
            print('书籍所在等级放大后的有效播放次数:',grade_amplify_playCount)
        if platform_base_billing_amount:
            # 等级1真实有效播放次数 * 等级1奖励倍数 + ... + 等级N真实有效播放次数 * 等级N奖励倍数
            grade_record = settlementAmount_sql_record[4]  # 某个平台的所有等级的播放次数和等级奖励倍数记录
            playCount_multiple = 0
            for every1 in grade_record:
                playCount_multiple += every1['SUM(pmpm.play_count )'] * Decimal(str(every1['award_multiple']))
            #整个平台当月播放单价，分后保留6位小数，多余小数截断
            if playCount_multiple:
                platform_play_price_original = platform_base_billing_amount / playCount_multiple
                platform_play_price_str = str(platform_play_price_original).split('.', 1)
                platform_play_price = Decimal(platform_play_price_str[0] + '.' + platform_play_price_str[1][0:6])
                print('平台当月播放单价：' + str(platform_play_price / 100))
            else:
                platform_play_price = 0
                print('平台当月播放单价：',0)
        else:
            platform_play_price=0
            print('平台当月播放单价：',platform_play_price)
        # 书籍所在等级的资金池金额
        if grade_amplify_playCount and platform_play_price:
            grade_pond_amount = grade_amplify_playCount * platform_play_price
            print('书籍所在等级的资金池金额:' + str(grade_pond_amount / 100))
        else:
            grade_pond_amount = 0
            print('书籍所在等级的资金池金额:',grade_pond_amount)

        # 某本书籍在某个平台的会员收入(原始值)
        # book_platform_amount=0  #初始化
        if book_playCount and grade_pond_amount:
            book_platform_amount_original = book_playCount * grade_pond_amount / grade_playCount
            book_platform_amount_original_str = str(book_platform_amount_original).split('.', 1)
            # 某个平台某本书的分成基数,精确到分，取整
            book_platform_divide_baseNum = book_platform_amount_original_str[0]
            book_platform_amount = Decimal(book_platform_divide_baseNum + '.' + book_platform_amount_original_str[1][0:6]) * book_days_rate
            book_platform_amount_final = str(book_platform_amount).split('.', 1)[0]
            # print(platform_play_price)
            print('会员书籍每月每本书的会员收入：' + str(book_platform_amount / 100))
            print('会员书籍每月每本书的本月可分成流水/分成基数：' + str(Decimal(book_platform_amount_final) / 100))
        else:
            book_platform_amount = 0
            book_platform_amount_final = 0
            print('会员书籍每月每本书的会员收入:',book_platform_amount)
            print('会员书籍每月每本书的分成基数/本月可分成流水：',book_platform_amount_final)
        '''查询合作方的分成比例、技术服务费率'''
        partner_record = settlementAmount_sql_record[5]#合作方信息
        if partner_record:
            cooperator_type = partner_record[0]['sp_type']  # 合作方类型 1渠道 2版权3主播 4分销商
            tech_service_rate = partner_record[0]['channel_rate']  # 版权/主播合作方的技术服务费比例
            if cooperator_type == 2:
                partner_rate = partner_record[0]['partner_rate']  # 版权合作方分成比例
                print('版权合作方分成比例：'+str(partner_rate))
            elif cooperator_type==3:
                Anch_partner_record = settlementAmount_sql_record[6][0]
                partner_rate = Anch_partner_record['share_fee_ratio']  # 主播合作方分成比例
                print('主播合作方分成比例：' + str(partner_rate))
            else:
                partner_rate=0
                book_platform_amount_final=0
                print('书籍每月分成基数/本月可分成流水：' + str(book_platform_amount_final))
                print('--------合作方为渠道合作方，请检查合作方id！！!----------')
                return {'partner_rate':partner_rate,'book_platform_amount_final':book_platform_amount_final}
        else:
            print("未查询到合作方或合作方无该业务！！！")
            # partner_rate=0
            tech_service_consumption = 0
            partner_divide_money = 0
            book_company_subsidy_money = 0
            partner_company_subsidy_money = 0
            partner_divide_money_final = 0
            print('懒人技术服务费(份额内）:', tech_service_consumption)
            print('预计合作方会员分成金额:',partner_divide_money)
            print('合作方书籍所属等级当月公司补贴金额:',book_company_subsidy_money)
            print('合作方当月公司补贴金额:',partner_company_subsidy_money)
            print('合作方分成金额/当月税前:',partner_divide_money_final)
            return {
                    'book_playCount':0,
                    'book_platform_amount_final':0,
                    'partner_divide_rate':0,
                    'partner_divide_money': 0,
                    'tech_service_consumption': 0,
                    'book_company_subsidy_money':0,
                    'partner_company_subsidy_money':0,
                    'partner_divide_money_final':0,
                    }
        # 合作方分成比例
        partner_divide_rate = partner_rate
        # 懒人技术服务费原始值(份额外）
        tech_service_consumption_original = book_platform_amount * tech_service_rate

        # 懒人技术服务费，进1(份额内）
        tech_service_consumption = math.ceil(tech_service_consumption_original * partner_divide_rate)
        # 合作方分成金额
        partner_divide_money_original = (book_platform_amount - book_platform_amount * tech_service_rate) * partner_divide_rate
        partner_divide_money_median = str(partner_divide_money_original).split('.', 1)
        # partner_divide_money = Decimal(partner_divide_money_median[0] + '.' + partner_divide_money_median[1][0:6])
        partner_divide_money = Decimal(partner_divide_money_median[0])
        print('懒人技术服务费(份额内）:' + str(tech_service_consumption / 100))
        print('预计合作方会员分成金额:' + str(partner_divide_money / 100))
        '''合作方书籍所属等级当月公司补贴金额'''
        #公司补贴百分比
        company_subsidy_percent = Decimal(settlementAmount_sql_record[7]) * Decimal('0.01')
        if company_subsidy_percent and settlementAmount_sql_record[8]:
            book_company_subsidy_money_original = platform_base_billing_amount * company_subsidy_percent * (settlementAmount_sql_record[8]* Decimal('0.01'))
            book_company_subsidy_money_median = str(book_company_subsidy_money_original).split('.', 1)
            book_company_subsidy_money = Decimal(book_company_subsidy_money_median[0] + '.' + book_company_subsidy_money_median[1][0:6])
            # book_company_subsidy_money=Decimal(book_company_subsidy_money_median[0])
            print('合作方书籍所属等级当月公司补贴金额:' + str(book_company_subsidy_money / 100))
            # 书籍当月的有效播放次数与书籍所属等级当月总的有效播放次数的比值
            if grade_playCount:
                book_grade_playCount_ratio_original = book_playCount / grade_playCount
            else:
                book_grade_playCount_ratio_original=0
            if book_grade_playCount_ratio_original:
                book_grade_playCount_ratio_median = str(book_grade_playCount_ratio_original).split('.', 1)
                book_grade_playCount_ratio = Decimal(book_grade_playCount_ratio_median[0] + '.' + book_grade_playCount_ratio_median[1][0:6])
            else:
                book_grade_playCount_ratio=0
            # 合作方当月公司补贴金额
            partner_company_subsidy_money_original = book_grade_playCount_ratio * book_company_subsidy_money*book_days_rate
            partner_company_subsidy_money_median = str(partner_company_subsidy_money_original).split('.', 1)
            # partner_company_subsidy_money_1 = partner_company_subsidy_money_median[0] + '.' + partner_company_subsidy_money_median[1][0:6]
            partner_company_subsidy_money=Decimal(partner_company_subsidy_money_median[0])
            print('合作方当月公司补贴金额:' + str(partner_company_subsidy_money / 100))
            # 合作方当月税前
            partner_divide_money_final = math.floor(partner_divide_money + partner_company_subsidy_money)
            print('合作方分成金额/当月税前：' + str(partner_divide_money_final / 100))
        else:
            book_company_subsidy_money = 0
            print('合作方书籍所属等级当月公司补贴金额:',book_company_subsidy_money)
            partner_company_subsidy_money = 0
            print('合作方当月公司补贴金额:',partner_company_subsidy_money)
            return {'book_company_subsidy_money':book_company_subsidy_money,'partner_company_subsidy_money':partner_company_subsidy_money}
        # 合作方当月税前
        partner_divide_money_final = math.floor(partner_divide_money + partner_company_subsidy_money)
        print('合作方分成金额/当月税前：' + str(partner_divide_money_final / 100))
        # return {'总流水(本月可分成流水/分成基数)':Decimal(book_platform_amount_final)/100,'书籍有效播放次数':book_playCount,'分成比例':partner_divide_rate,'分成金额':Decimal(partner_divide_money_final)/100,'懒人技术服务费':Decimal(tech_service_consumption)/100}
        return {'book_platform_amount_final': str(Decimal(book_platform_amount_final) / 100),
                'book_playCount': str(book_playCount),
                'partner_divide_rate': str(partner_divide_rate),
                'partner_divide_money_final': str(Decimal(partner_divide_money_final) / 100),
                'tech_service_consumption': str(Decimal(tech_service_consumption) / 100)}
        # return [book_playCount,Decimal(book_platform_amount_final)/100,Decimal(tech_service_consumption)/100,partner_divide_money/100,Decimal(partner_company_subsidy_money)/100,Decimal(partner_divide_money_final)/100]

    def book_settlement_amount(self):
        '''计算书籍在懒人和芽芽会员收入'''
        #懒人听书平台会员书籍每月每本书的会员收入
        print('-----------懒人听书-------------------')
        lr=self.platform_book_settlement_amount(1)
        #芽芽故事平台会员书籍每月每本书的会员收入
        print('-----------芽芽故事-------------------')
        yaya=self.platform_book_settlement_amount(2)
        book_platform_divide_baseNum=lr['book_platform_amount_final']+yaya['book_platform_amount_final']
        book_playCount = lr['book_playCount'] + yaya['book_playCount']
        tech_service_consumption=lr['tech_service_consumption']+yaya['tech_service_consumption']
        partner_divide_money_final=lr['partner_divide_money_final']+yaya['partner_divide_money_final']
        print('-------------懒人听书+芽芽故事-------------')
        print('合作方id:' + str(self.partner_id) + '|' + '资源id:' + str(self.entity_id))
        print('懒人+芽芽的书籍当月有效播放次数：' + str(book_playCount))
        print('懒人+芽芽的本月可分成流水/分成基数：'+str(book_platform_divide_baseNum))
        print('懒人+芽芽的技术服务费：'+str(tech_service_consumption))
        print('懒人+芽芽的分成金额/当月税前：'+str(partner_divide_money_final))

class Channel_Settlement():

    def __init__(self,settlement_month,partner_id):
        self.settlement_month = settlement_month
        self.partner_id=partner_id

    def channel_platform_book_settlement_amount(self,product_type=1):
        '''渠道合作方结算计算'''
        date_style = str(self.settlement_month)
        year_month = date_style[0:4] + '-' + date_style[4:6]
        # 结算开始时间
        start_time = year_month + '-01'+' 0:00:00'
        print(start_time)
        # 根据传入的结算月份得到结算结束时间
        days = month_days(date_style)
        end_time = year_month + '-' + str(days)+' 23:59:59'
        print(end_time)

        #当前月该渠道合作方所有的会员订单
        member_order_item=billing_select('''SELECT * from p_member_order_item pmoi 
                                                   where product_type=%s and channel_partner_id =%s and create_time BETWEEN '%s' and '%s'and status=0 and channel_amount >0;'''%(product_type,self.partner_id,start_time,end_time),'billing')
        #数据初始化
        can_divide_amount=0
        pay_amount_in=0
        channel_lr_amount_in=0
        settlement_amount_original=0
        divide_baseAmount_final=0
        for every_order_item in member_order_item:
            can_divide_amount+=every_order_item['total_fee'] # 本月实际流水/本月可分成流水
            pay_amount_out=every_order_item['total_fee']*every_order_item['pay_rate'] #第三方支付手续费(份额外）
            pay_amount_in+=math.ceil(every_order_item['total_fee']*every_order_item['pay_rate']*every_order_item['channel_rate']) #第三方支付手续费(份额内）
            # 分成基数
            divide_baseAmount_original = every_order_item['total_fee'] - pay_amount_out
            divide_baseAmount_str=str(divide_baseAmount_original).split('.',1)
            divide_baseAmount=Decimal(divide_baseAmount_str[0]+'.'+divide_baseAmount_str[1][0:6])
            divide_baseAmount_final+=divide_baseAmount
            channel_lr_amount_out=divide_baseAmount_original*every_order_item['channel_lr_rate'] #懒人技术服务费（份额外）
            channel_lr_amount_in+=math.ceil(divide_baseAmount_original*every_order_item['channel_lr_rate']*every_order_item['channel_rate']) #懒人技术服务费（份额内）
            #分成金额
            settlement_amount_original+=(divide_baseAmount_original-channel_lr_amount_out)*every_order_item['channel_rate']
            settlement_amount_original=str(settlement_amount_original).split('.',1)
            settlement_amount_original=Decimal(settlement_amount_original[0]+'.'+settlement_amount_original[1][0:6])
        #渠道合作方分成基数
        divide_baseAmount_final=math.floor(divide_baseAmount_final)
        #渠道合作方结算金额/分成金额
        settlement_amount=math.floor(settlement_amount_original)
        # print('合作方id:' + str(self.partner_id) + '|' + '资源id:' + str(self.entity_id))
        print('结算月份:'+str(self.settlement_month))
        print('合作方id:' + str(self.partner_id) )
        print('本月实际流水/本月可分成流水:' + str(can_divide_amount/100))
        print('第三方支付手续费：' + str(pay_amount_in / 100))
        print('渠道合作方分成基数:' + str(divide_baseAmount_final/100))
        print('懒人技术服务费：' + str(channel_lr_amount_in/100))
        print('渠道分成金额/当月税前：' + str(settlement_amount/100))
        return {'settlement_month':str(self.settlement_month),'partner_id':str(self.partner_id),'can_divide_amount':str(can_divide_amount/100),
                'pay_amount_in':str(pay_amount_in/100),'divide_baseAmount_final':str(divide_baseAmount_final/100),
                'channel_lr_amount_in':str(channel_lr_amount_in/100),'settlement_amount':str(settlement_amount/100)}
        # return [str(can_divide_amount/100),str(divide_baseAmount_final/100),str(pay_amount_in/100),str(channel_lr_amount_in/100),str(settlement_amount/100)]

    def channel_book_settlement_amount(self):
        '''渠道合作方懒人+芽芽结算数据'''
        # 懒人听书平台会员书籍每月每本书的会员收入
        print('-----------懒人听书-------------------')
        lr = self.channel_platform_book_settlement_amount(1)
        # 芽芽故事平台会员书籍每月每本书的会员收入
        print('-----------芽芽故事-------------------')
        yaya = self.channel_platform_book_settlement_amount(2)
        can_divide_amount = Decimal(lr[0]) + Decimal(yaya[0])
        divide_baseAmount_final=Decimal(lr[1])+Decimal(lr[1])
        pay_amount_in=Decimal(lr[2])+Decimal(lr[2])
        channel_lr_amount_in = Decimal(lr[3]) + Decimal(yaya[3])
        settlement_amount = Decimal(lr[4]) + Decimal(yaya[4])
        print('-------------懒人听书+芽芽故事-------------')
        print('合作方id:'+str(self.partner_id)+'|'+'资源id:'+str(self.entity_id))
        print('本月实际流水/本月可分成流水:'+str(can_divide_amount/100))
        print('懒人+芽芽的分成基数：'+str(divide_baseAmount_final/100))
        print('懒人+芽芽的第三方支付手续费：' + str(pay_amount_in/100))
        print('懒人+芽芽的技术服务费：' + str(channel_lr_amount_in/100))
        print('懒人+芽芽的分成金额/当月税前：' + str(settlement_amount/100))


if __name__=='__main__':
    #版权/主播合作方 分别传入结算月份，书籍id，合作方id,以及合作方当月分成天数占比
    SettlementVIP(202009,931,1899,1).platform_book_settlement_amount()
    # SettlementVIP(202007,930,1695,0.096774).platform_book_settlement_amount()
    # 渠道合作方 分成传入结算月份，合作方id
    # Channel_Settlement(202008,1666).channel_platform_book_settlement_amount()
    # SettlementVIP(202006,32945,1459,1).adjust_percent()



