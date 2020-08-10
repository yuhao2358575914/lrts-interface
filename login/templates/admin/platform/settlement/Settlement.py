# coding=gbk
from login.templates.admin.platform.common.operate_mysql import billing_select
from decimal import *
from login.templates.admin.platform.settlement.get_CurrentTime import getCurrentTime, month_days
import math


class Settlement(object):
    '''结算类'''

    def __init__(self,settlement_month,entity_id,partner_id,sp_type):
        '''
        :param entity_id: 书籍id
        :param partner_id 合作方id
        :param sp_type: 1电子阅读 2付费收听 4主播打赏  8漫画
        '''
        self.settlement_month=settlement_month
        self.entity_id=entity_id
        self.partner_id=partner_id
        self.sp_type=sp_type
    def settlement_lr_yaya(self,product_type=1):
        '''结算懒人/芽芽
        :param product_type 1懒人 2芽芽
        '''
        date_style = str(self.settlement_month)
        year_month = date_style[0:4] + '-' + date_style[4:6]
        # 结算开始时间
        start_time = year_month + '-01'
        print(start_time)
        #根据传入的结算月份得到结算结束时间
        input_month=date_style[0:6]
        current_time_record=getCurrentTime()
        current_month=current_time_record[2]
        if input_month==current_month:
            end_time=current_time_record[0]
            print(end_time)
        else:
            days = month_days(date_style)
            end_time = year_month + '-' + str(days)
            print(end_time)
        #判断合作方的合作业务
        if self.sp_type==1:
            business='电子阅读'
        elif self.sp_type==2:
            business='付费收听'
        elif self.sp_type==4:
            business='主播打赏'
        elif self.sp_type==8:
            business='漫画'
        '''查询版权/主播/渠道合作方的相关分成信息'''
        partner_record = billing_select("SELECT * from billing.p_partner_service where partner_id='%s' and service_type=%s ORDER BY id desc LIMIT 1" % (self.partner_id,self.sp_type), "billing")
        if partner_record:
            cooperator_type=partner_record[0]['sp_type'] #合作方类型 1渠道 2版权3主播 4分销商
            tech_service_rate = partner_record[0]['channel_rate']  # 版权/渠道/主播合作方的技术服务费比例
            if cooperator_type == 1 or cooperator_type == 2:
                partner_rate = partner_record[0]['partner_rate']  # 版权/渠道合作方分成比例
            else:
                if self.sp_type == 2 or self.sp_type == 5:
                    Anch_partner_record = billing_select("select * from p_share_fee_resource where res_id = '%s' and share_fee_type = 2 order by create_time desc limit 1;" % (
                            self.entity_id), "billing")
                    partner_rate = Anch_partner_record[0]['share_fee_ratio']  # 主播合作方分成比例
                    # print('--------------------'+str(rate['partner_rate']))
                elif self.sp_type == 4 or self.sp_type == 5:
                    Anch_partner_record = billing_select("select * from p_share_fee_resource where res_id = '%s' and share_fee_type = 1 order by create_time desc limit 1;" % (
                            self.entity_id), "billing")
                    partner_rate = Anch_partner_record[0]['share_fee_ratio']  # 主播合作方分成比例
                else:
                    pass
        else:
            print("未查询到合作方或合作方无该业务！！！")
            return {'lr_sum_cash_flow': 0,
                    'lr_sum_cash_flow_billing': 0,
                    'lr_channel_partner_amount': 0,
                    'lr_sum_commission_in': 0,
                    'lr_base_billing_amount': 0,
                    'lr_partner_amount': 0,
                    'lr_tech_amount': 0,
                    'baseBillingAounmt_subtract_techAmount': 0
                    }

        #---测试环境表名为:p_resource_daily_billing,预发布环境表名为：test_resource_daily_billing----
        lr_cp_daily_info = billing_select(''' SELECT * FROM p_resource_daily_billing
                                            WHERE entity_id='%s' and partner_id='%s'and sp_type='%s' and  product_type='%s'and billing_date between '%s' and '%s' ORDER BY create_time desc ;'''
                                          % (self.entity_id, self.partner_id, self.sp_type, product_type,start_time,end_time), "billing")
        if lr_cp_daily_info:
            lr_sum_cash_flow_billing_1 = 0
            lr_sum_cash_flow_billing_2 = 0
            lr_sum_commission_out = 0
            lr_sum_cash_flow = 0
            for day in lr_cp_daily_info:
                lr_sum_cash_flow += day['sum_cash_flow']  # 统计本月实际流水
                channel_partner_id=day['channel_partner_id'] #查看关联的渠道合作方id
                if channel_partner_id:
                    channel_partner_rate=day['channel_partner_rate']
                    lr_sum_cash_flow_billing_1 += math.floor(day['sum_cash_flow']*(1-channel_partner_rate)) # 统计本月可分成流水
                else:
                    lr_sum_cash_flow_billing_2+=day['sum_cash_flow'] # 统计本月可分成流水
                sum_cash_flow_billing=lr_sum_cash_flow_billing_1+lr_sum_cash_flow_billing_2
                commission_id = day['commission_id'] #获取手续费率id
                #测试环境切换成这个sql
                pay_rate=billing_select("SELECT * from p_billing_records_commission where id='%s';" %(commission_id),'billing') #根据commission_id查询相对应的手续费明细
                #预发布切换成这个sql
                # pay_rate=billing_select("SELECT * from test_billing_records_commission where id='%s';" %(commission_id),'billing') #根据commission_id查询相对应的手续费明细
                # 统计份额外支付手续费
                lr_sum_commission_out +=Decimal(day['and_wx_cash_flow_billing']) * pay_rate[0]['wx_pay_rate'] + Decimal(day['and_ali_cash_flow_billing']) * pay_rate[0]['ali_pay_rate'] + Decimal(day['and_hw_cash_flow_billing']) * pay_rate[0]['hw_pay_rate'] + \
                                        Decimal(day['and_vivo_cash_flow_billing']) * pay_rate[0]['vivo_pay_rate'] + Decimal(day['and_oppo_cash_flow_billing']) * pay_rate[0]['oppo_pay_rate'] + Decimal(day['and_meizu_cash_flow_billing']) * pay_rate[0]['meizu_pay_rate'] + \
                                        Decimal(day['and_xiaomi_cash_flow_billing']) * pay_rate[0]['xiaomi_pay_rate'] + Decimal(day['and_ccb_cash_flow_billing']) * pay_rate[0]['ccb_pay_rate'] + Decimal(day['and_abc_cash_flow_billing']) * pay_rate[0]['abc_pay_rate'] + \
                                        Decimal(day['and_lr_cash_flow_billing']) * pay_rate[0]['lr_pay_rate'] + Decimal(day['ios_wx_cash_flow_billing']) * pay_rate[0]['wx_pay_rate'] + Decimal(day['ios_ali_cash_flow_billing']) * pay_rate[0]['ali_pay_rate'] + \
                                        Decimal(day['ios_lr_cash_flow_billing']) * pay_rate[0]['ios_pay_rate'] + Decimal(day['ios_ccb_cash_flow_billing']) * pay_rate[0]['ccb_pay_rate'] + Decimal(day['ios_abc_cash_flow_billing']) * pay_rate[0]['abc_pay_rate'] + \
                                        Decimal(day['fulu_cash_flow_billing']) * pay_rate[0]['lr_pay_rate']
        else:
            lr_sum_cash_flow=0
            lr_sum_cash_flow_billing=0
            lr_channel_partner_amount=0
            lr_sum_commission_in=0
            lr_base_billing_amount=0
            lr_partner_amount=0
            lr_tech_amount=0
            baseBillingAounmt_subtract_techAmount=0
            print('合作方书籍无日结数据！！！')
            return {'lr_sum_cash_flow': str(lr_sum_cash_flow / 100),
                    'lr_sum_cash_flow_billing': str(lr_sum_cash_flow_billing / 100),
                    'lr_channel_partner_amount': str(lr_channel_partner_amount / 100),
                    'lr_sum_commission_in': str(lr_sum_commission_in / 100),
                    'lr_base_billing_amount': str(lr_base_billing_amount / 100),
                    'lr_partner_amount': str(lr_partner_amount / 100),
                    'lr_tech_amount': str(lr_tech_amount / 100),
                    'baseBillingAounmt_subtract_techAmount': str(baseBillingAounmt_subtract_techAmount / 100)
                    }
        # 份额内支付手续费（原始值）、份额内支付手续费（进1）
        lr_sum_commission_in_original = lr_sum_commission_out * partner_rate
        lr_sum_commission_in = math.ceil(lr_sum_commission_in_original)
        # 本月可分成流水
        lr_sum_cash_flow_billing = sum_cash_flow_billing
        # 渠道分成金额
        lr_channel_partner_amount = lr_sum_cash_flow - lr_sum_cash_flow_billing
        # 计算分成基数(原始值）、分成基数（截断）
        lr_base_billing_amount_original = lr_sum_cash_flow_billing - lr_sum_commission_out  # 本月可分成流水 - 本月可分成流水*支付手续费率（本月可分成流水-支付手续费（份额外））
        lr_base_billing_amount = math.floor(lr_base_billing_amount_original)
        # 当月税前(原始值）、当月税前（截断）
        lr_partner_amount_original = (lr_base_billing_amount_original - lr_base_billing_amount_original * tech_service_rate) * partner_rate  # 版权分成金额=（分成基数-懒人技术服务费）* 版权分成比例
        lr_partner_amount = math.floor(lr_partner_amount_original)
        # 技术服务费(原始值）、技术服务费(进1）
        lr_tech_amount_original = lr_base_billing_amount_original * tech_service_rate * partner_rate  # 技术服务费=分成基数 * 懒人技术服务费率*版权分成比例
        lr_tech_amount = math.ceil(lr_tech_amount_original)
        #（分成基数-懒人技术服务费）原始值、（分成基数-懒人技术服务费）截断
        baseBillingAounmt_subtract_techAmount_Original=lr_base_billing_amount_original-lr_base_billing_amount_original * tech_service_rate
        baseBillingAounmt_subtract_techAmount = math.floor(baseBillingAounmt_subtract_techAmount_Original)
        print('结算月份为:',self.settlement_month,'合作方id为',self.partner_id,'合作方资源id为:',self.entity_id,'合作方业务为:',business)
        print('本月实际流水:' + str(lr_sum_cash_flow / 100) + '|' + '本月可分成流水：' + str(lr_sum_cash_flow_billing / 100))
        print('渠道分成金额：' + str(lr_channel_partner_amount / 100))
        print('支付手续费(原始值）：' + str(lr_sum_commission_in_original / 100) + '|' + '支付手续费：' + str(lr_sum_commission_in / 100))
        print('分成基数(原始值）：' + str(lr_base_billing_amount_original / 100) + '|' + '分成基数：' + str(lr_base_billing_amount / 100))
        print('当月税前(原始值）:' + str(lr_partner_amount_original / 100) + '|' + '当月税前：' + str(lr_partner_amount / 100))
        print('懒人技术服务费(原始值）:' + str(lr_tech_amount_original / 100) + '|' + '懒人技术服务费' + str(lr_tech_amount / 100))
        print('分成基数-懒人技术服务费(原始值)：'+str(baseBillingAounmt_subtract_techAmount_Original/100)+'|'+'分成基数-懒人技术服务费：'+str(baseBillingAounmt_subtract_techAmount/100))
        # return [str(lr_sum_cash_flow / 100),str(lr_sum_cash_flow_billing / 100),str(lr_channel_partner_amount / 100),str(lr_sum_commission_in_original / 100),str(lr_sum_commission_in / 100),
        #         str(lr_base_billing_amount_original / 100),str(lr_base_billing_amount / 100),str(lr_partner_amount_original / 100),str(lr_partner_amount / 100),
        #         str(lr_tech_amount_original / 100),str(lr_tech_amount / 100),str(baseBillingAounmt_subtract_techAmount_Original/100),str(baseBillingAounmt_subtract_techAmount/100)]
        return {'settlement_month':self.settlement_month,'partner_id':self.partner_id,'entity_id':self.entity_id,'business':business,
                'lr_sum_cash_flow': str(lr_sum_cash_flow/100), 'lr_sum_cash_flow_billing': str(lr_sum_cash_flow_billing/100),
                'lr_channel_partner_amount': str(lr_channel_partner_amount/100),
                 'lr_sum_commission_in': str(lr_sum_commission_in/100),
                'lr_base_billing_amount':str(lr_base_billing_amount/100),
                'lr_partner_amount': str(lr_partner_amount/100),
                'lr_tech_amount': str(lr_tech_amount/100),
                'baseBillingAounmt_subtract_techAmount': str(baseBillingAounmt_subtract_techAmount/100)
                }
    def settlement_partner(self):
        '''版权合作方结算(懒人+芽芽)'''
        print('---------------------------------懒人听书-------------------------------')
        lr_list=self.settlement_lr_yaya(1)
        print('---------------------------------芽芽故事-------------------------------')
        yaya_list=self.settlement_lr_yaya(2)
        #本月实际流水
        sum_cash_flow=Decimal(lr_list['lr_sum_cash_flow'])+Decimal(yaya_list['lr_sum_cash_flow'])
        #本月可分成流水
        sum_cash_flow_billing = Decimal(lr_list['lr_sum_cash_flow_billing'])+Decimal(yaya_list['lr_sum_cash_flow_billing'])
        #渠道分成金额
        channel_partner_amount=Decimal(lr_list['lr_channel_partner_amount'])+Decimal(yaya_list['lr_channel_partner_amount'])
        # 份额内支付手续费（进1）
        sum_commission = Decimal(lr_list['lr_sum_commission_in']) + Decimal(yaya_list['lr_sum_commission_in'])
        #分成基数（截断）--本月可分成流水 - 本月可分成流水*支付手续费率（本月可分成流水-支付手续费（份额外））
        base_billing_amount=Decimal(lr_list['lr_base_billing_amount'])+Decimal(yaya_list['lr_base_billing_amount'])
        #当月税前（截断）版权分成金额=（分成基数-懒人技术服务费）* 版权分成比例
        partner_amount=Decimal(lr_list['lr_partner_amount'])+Decimal(yaya_list['lr_partner_amount'])
        # 技术服务费(进1）技术服务费=分成基数 * 懒人技术服务费率*版权分成比例
        tech_amount = Decimal(lr_list['lr_tech_amount'])+Decimal(yaya_list['lr_tech_amount'])
        # (分成基数-懒人技术服务费）截断
        baseBillingAounmt_subtract_techAmount = Decimal(lr_list['baseBillingAounmt_subtract_techAmount'])+Decimal(yaya_list['baseBillingAounmt_subtract_techAmount'])

        print('-------------------------------懒人听书+芽芽故事--------------------------------------')
        print('本月实际流水:'+str(sum_cash_flow)+'|'+'本月可分成流水：'+str(sum_cash_flow_billing))
        print('渠道分成金额：'+str(channel_partner_amount))
        print('支付手续费：'+str(sum_commission))
        print('分成基数：'+str(base_billing_amount))
        print('当月税前：'+str(partner_amount))
        print('懒人技术服务费' + str(tech_amount))
        print('分成基数-懒人技术服务费：' + str(baseBillingAounmt_subtract_techAmount))
        return {'sum_cash_flow':str(sum_cash_flow),'sum_cash_flow_billing':str(sum_cash_flow_billing),
                'channel_partner_amount':str(channel_partner_amount),
                'sum_commission':str(sum_commission),
                'base_billing_amount':str(base_billing_amount),
                'partner_amount':str(partner_amount),'tech_amount':str(tech_amount),
                'baseBillingAounmt_subtract_techAmount':str(baseBillingAounmt_subtract_techAmount)
                }


if __name__=="__main__":
    # Settlement().cp_settlement(33214,2)
    '''依次传入资源id，合作方id，合作业务(1电子阅读 2付费收听 4主播打赏  8漫画)'''
    # Settlement(92426468, 1489,4).settlement_partner()
    Settlement(202006,33215,1596,2).settlement_partner()
    # Settlement(147, 1638, 8).settlement_partner()

