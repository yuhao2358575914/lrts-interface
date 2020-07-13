#生成一个新的手机号
import random
def create_PhoneNum():
    '''生成一个手机号'''
    phone_1='1'
    phone_2=random.randint(1000000000,9999999999)
    phoneNum=phone_1+str(phone_2)
    # print(phoneNum)
    return phoneNum
def create_IDNumber():
    '''生成身份证号'''
    IDNumber=random.randint(100000000000000000,999999999999999999)
    # print(IDNumber)
    return IDNumber
def create_CreditCardNumbers():
    '''生成银行卡号'''
    CreditCardNumbers = random.randint(1000000000000000000, 9999999999999999999)
    # print(IDNumber)
    return CreditCardNumbers
if __name__=='__main__':
    create_PhoneNum()
