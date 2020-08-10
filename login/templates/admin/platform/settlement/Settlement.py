# coding=gbk
from login.templates.admin.platform.common.operate_mysql import billing_select
from decimal import *
from login.templates.admin.platform.settlement.get_CurrentTime import getCurrentTime, month_days
import math


class Settlement(object):
    '''������'''

    def __init__(self,settlement_month,entity_id,partner_id,sp_type):
        '''
        :param entity_id: �鼮id
        :param partner_id ������id
        :param sp_type: 1�����Ķ� 2�������� 4��������  8����
        '''
        self.settlement_month=settlement_month
        self.entity_id=entity_id
        self.partner_id=partner_id
        self.sp_type=sp_type
    def settlement_lr_yaya(self,product_type=1):
        '''��������/ѿѿ
        :param product_type 1���� 2ѿѿ
        '''
        date_style = str(self.settlement_month)
        year_month = date_style[0:4] + '-' + date_style[4:6]
        # ���㿪ʼʱ��
        start_time = year_month + '-01'
        print(start_time)
        #���ݴ���Ľ����·ݵõ��������ʱ��
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
        #�жϺ������ĺ���ҵ��
        if self.sp_type==1:
            business='�����Ķ�'
        elif self.sp_type==2:
            business='��������'
        elif self.sp_type==4:
            business='��������'
        elif self.sp_type==8:
            business='����'
        '''��ѯ��Ȩ/����/��������������طֳ���Ϣ'''
        partner_record = billing_select("SELECT * from billing.p_partner_service where partner_id='%s' and service_type=%s ORDER BY id desc LIMIT 1" % (self.partner_id,self.sp_type), "billing")
        if partner_record:
            cooperator_type=partner_record[0]['sp_type'] #���������� 1���� 2��Ȩ3���� 4������
            tech_service_rate = partner_record[0]['channel_rate']  # ��Ȩ/����/�����������ļ�������ѱ���
            if cooperator_type == 1 or cooperator_type == 2:
                partner_rate = partner_record[0]['partner_rate']  # ��Ȩ/�����������ֳɱ���
            else:
                if self.sp_type == 2 or self.sp_type == 5:
                    Anch_partner_record = billing_select("select * from p_share_fee_resource where res_id = '%s' and share_fee_type = 2 order by create_time desc limit 1;" % (
                            self.entity_id), "billing")
                    partner_rate = Anch_partner_record[0]['share_fee_ratio']  # �����������ֳɱ���
                    # print('--------------------'+str(rate['partner_rate']))
                elif self.sp_type == 4 or self.sp_type == 5:
                    Anch_partner_record = billing_select("select * from p_share_fee_resource where res_id = '%s' and share_fee_type = 1 order by create_time desc limit 1;" % (
                            self.entity_id), "billing")
                    partner_rate = Anch_partner_record[0]['share_fee_ratio']  # �����������ֳɱ���
                else:
                    pass
        else:
            print("δ��ѯ����������������޸�ҵ�񣡣���")
            return {'lr_sum_cash_flow': 0,
                    'lr_sum_cash_flow_billing': 0,
                    'lr_channel_partner_amount': 0,
                    'lr_sum_commission_in': 0,
                    'lr_base_billing_amount': 0,
                    'lr_partner_amount': 0,
                    'lr_tech_amount': 0,
                    'baseBillingAounmt_subtract_techAmount': 0
                    }

        #---���Ի�������Ϊ:p_resource_daily_billing,Ԥ������������Ϊ��test_resource_daily_billing----
        lr_cp_daily_info = billing_select(''' SELECT * FROM p_resource_daily_billing
                                            WHERE entity_id='%s' and partner_id='%s'and sp_type='%s' and  product_type='%s'and billing_date between '%s' and '%s' ORDER BY create_time desc ;'''
                                          % (self.entity_id, self.partner_id, self.sp_type, product_type,start_time,end_time), "billing")
        if lr_cp_daily_info:
            lr_sum_cash_flow_billing_1 = 0
            lr_sum_cash_flow_billing_2 = 0
            lr_sum_commission_out = 0
            lr_sum_cash_flow = 0
            for day in lr_cp_daily_info:
                lr_sum_cash_flow += day['sum_cash_flow']  # ͳ�Ʊ���ʵ����ˮ
                channel_partner_id=day['channel_partner_id'] #�鿴����������������id
                if channel_partner_id:
                    channel_partner_rate=day['channel_partner_rate']
                    lr_sum_cash_flow_billing_1 += math.floor(day['sum_cash_flow']*(1-channel_partner_rate)) # ͳ�Ʊ��¿ɷֳ���ˮ
                else:
                    lr_sum_cash_flow_billing_2+=day['sum_cash_flow'] # ͳ�Ʊ��¿ɷֳ���ˮ
                sum_cash_flow_billing=lr_sum_cash_flow_billing_1+lr_sum_cash_flow_billing_2
                commission_id = day['commission_id'] #��ȡ��������id
                #���Ի����л������sql
                pay_rate=billing_select("SELECT * from p_billing_records_commission where id='%s';" %(commission_id),'billing') #����commission_id��ѯ���Ӧ����������ϸ
                #Ԥ�����л������sql
                # pay_rate=billing_select("SELECT * from test_billing_records_commission where id='%s';" %(commission_id),'billing') #����commission_id��ѯ���Ӧ����������ϸ
                # ͳ�Ʒݶ���֧��������
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
            print('�������鼮���ս����ݣ�����')
            return {'lr_sum_cash_flow': str(lr_sum_cash_flow / 100),
                    'lr_sum_cash_flow_billing': str(lr_sum_cash_flow_billing / 100),
                    'lr_channel_partner_amount': str(lr_channel_partner_amount / 100),
                    'lr_sum_commission_in': str(lr_sum_commission_in / 100),
                    'lr_base_billing_amount': str(lr_base_billing_amount / 100),
                    'lr_partner_amount': str(lr_partner_amount / 100),
                    'lr_tech_amount': str(lr_tech_amount / 100),
                    'baseBillingAounmt_subtract_techAmount': str(baseBillingAounmt_subtract_techAmount / 100)
                    }
        # �ݶ���֧�������ѣ�ԭʼֵ�����ݶ���֧�������ѣ���1��
        lr_sum_commission_in_original = lr_sum_commission_out * partner_rate
        lr_sum_commission_in = math.ceil(lr_sum_commission_in_original)
        # ���¿ɷֳ���ˮ
        lr_sum_cash_flow_billing = sum_cash_flow_billing
        # �����ֳɽ��
        lr_channel_partner_amount = lr_sum_cash_flow - lr_sum_cash_flow_billing
        # ����ֳɻ���(ԭʼֵ�����ֳɻ������ضϣ�
        lr_base_billing_amount_original = lr_sum_cash_flow_billing - lr_sum_commission_out  # ���¿ɷֳ���ˮ - ���¿ɷֳ���ˮ*֧���������ʣ����¿ɷֳ���ˮ-֧�������ѣ��ݶ��⣩��
        lr_base_billing_amount = math.floor(lr_base_billing_amount_original)
        # ����˰ǰ(ԭʼֵ��������˰ǰ���ضϣ�
        lr_partner_amount_original = (lr_base_billing_amount_original - lr_base_billing_amount_original * tech_service_rate) * partner_rate  # ��Ȩ�ֳɽ��=���ֳɻ���-���˼�������ѣ�* ��Ȩ�ֳɱ���
        lr_partner_amount = math.floor(lr_partner_amount_original)
        # ���������(ԭʼֵ�������������(��1��
        lr_tech_amount_original = lr_base_billing_amount_original * tech_service_rate * partner_rate  # ���������=�ֳɻ��� * ���˼����������*��Ȩ�ֳɱ���
        lr_tech_amount = math.ceil(lr_tech_amount_original)
        #���ֳɻ���-���˼�������ѣ�ԭʼֵ�����ֳɻ���-���˼�������ѣ��ض�
        baseBillingAounmt_subtract_techAmount_Original=lr_base_billing_amount_original-lr_base_billing_amount_original * tech_service_rate
        baseBillingAounmt_subtract_techAmount = math.floor(baseBillingAounmt_subtract_techAmount_Original)
        print('�����·�Ϊ:',self.settlement_month,'������idΪ',self.partner_id,'��������ԴidΪ:',self.entity_id,'������ҵ��Ϊ:',business)
        print('����ʵ����ˮ:' + str(lr_sum_cash_flow / 100) + '|' + '���¿ɷֳ���ˮ��' + str(lr_sum_cash_flow_billing / 100))
        print('�����ֳɽ�' + str(lr_channel_partner_amount / 100))
        print('֧��������(ԭʼֵ����' + str(lr_sum_commission_in_original / 100) + '|' + '֧�������ѣ�' + str(lr_sum_commission_in / 100))
        print('�ֳɻ���(ԭʼֵ����' + str(lr_base_billing_amount_original / 100) + '|' + '�ֳɻ�����' + str(lr_base_billing_amount / 100))
        print('����˰ǰ(ԭʼֵ��:' + str(lr_partner_amount_original / 100) + '|' + '����˰ǰ��' + str(lr_partner_amount / 100))
        print('���˼��������(ԭʼֵ��:' + str(lr_tech_amount_original / 100) + '|' + '���˼��������' + str(lr_tech_amount / 100))
        print('�ֳɻ���-���˼��������(ԭʼֵ)��'+str(baseBillingAounmt_subtract_techAmount_Original/100)+'|'+'�ֳɻ���-���˼�������ѣ�'+str(baseBillingAounmt_subtract_techAmount/100))
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
        '''��Ȩ����������(����+ѿѿ)'''
        print('---------------------------------��������-------------------------------')
        lr_list=self.settlement_lr_yaya(1)
        print('---------------------------------ѿѿ����-------------------------------')
        yaya_list=self.settlement_lr_yaya(2)
        #����ʵ����ˮ
        sum_cash_flow=Decimal(lr_list['lr_sum_cash_flow'])+Decimal(yaya_list['lr_sum_cash_flow'])
        #���¿ɷֳ���ˮ
        sum_cash_flow_billing = Decimal(lr_list['lr_sum_cash_flow_billing'])+Decimal(yaya_list['lr_sum_cash_flow_billing'])
        #�����ֳɽ��
        channel_partner_amount=Decimal(lr_list['lr_channel_partner_amount'])+Decimal(yaya_list['lr_channel_partner_amount'])
        # �ݶ���֧�������ѣ���1��
        sum_commission = Decimal(lr_list['lr_sum_commission_in']) + Decimal(yaya_list['lr_sum_commission_in'])
        #�ֳɻ������ضϣ�--���¿ɷֳ���ˮ - ���¿ɷֳ���ˮ*֧���������ʣ����¿ɷֳ���ˮ-֧�������ѣ��ݶ��⣩��
        base_billing_amount=Decimal(lr_list['lr_base_billing_amount'])+Decimal(yaya_list['lr_base_billing_amount'])
        #����˰ǰ���ضϣ���Ȩ�ֳɽ��=���ֳɻ���-���˼�������ѣ�* ��Ȩ�ֳɱ���
        partner_amount=Decimal(lr_list['lr_partner_amount'])+Decimal(yaya_list['lr_partner_amount'])
        # ���������(��1�����������=�ֳɻ��� * ���˼����������*��Ȩ�ֳɱ���
        tech_amount = Decimal(lr_list['lr_tech_amount'])+Decimal(yaya_list['lr_tech_amount'])
        # (�ֳɻ���-���˼�������ѣ��ض�
        baseBillingAounmt_subtract_techAmount = Decimal(lr_list['baseBillingAounmt_subtract_techAmount'])+Decimal(yaya_list['baseBillingAounmt_subtract_techAmount'])

        print('-------------------------------��������+ѿѿ����--------------------------------------')
        print('����ʵ����ˮ:'+str(sum_cash_flow)+'|'+'���¿ɷֳ���ˮ��'+str(sum_cash_flow_billing))
        print('�����ֳɽ�'+str(channel_partner_amount))
        print('֧�������ѣ�'+str(sum_commission))
        print('�ֳɻ�����'+str(base_billing_amount))
        print('����˰ǰ��'+str(partner_amount))
        print('���˼��������' + str(tech_amount))
        print('�ֳɻ���-���˼�������ѣ�' + str(baseBillingAounmt_subtract_techAmount))
        return {'sum_cash_flow':str(sum_cash_flow),'sum_cash_flow_billing':str(sum_cash_flow_billing),
                'channel_partner_amount':str(channel_partner_amount),
                'sum_commission':str(sum_commission),
                'base_billing_amount':str(base_billing_amount),
                'partner_amount':str(partner_amount),'tech_amount':str(tech_amount),
                'baseBillingAounmt_subtract_techAmount':str(baseBillingAounmt_subtract_techAmount)
                }


if __name__=="__main__":
    # Settlement().cp_settlement(33214,2)
    '''���δ�����Դid��������id������ҵ��(1�����Ķ� 2�������� 4��������  8����)'''
    # Settlement(92426468, 1489,4).settlement_partner()
    Settlement(202006,33215,1596,2).settlement_partner()
    # Settlement(147, 1638, 8).settlement_partner()

