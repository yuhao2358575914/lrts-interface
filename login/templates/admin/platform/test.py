from login.templates.admin.platform.common.operate_mysql import billing_select


def testtt():
    # company_subsidy_percent = billing_select("select * from p_config_server pcs where config_key ='COMPANY_SUBSIDY_PERCENT';", 'billing')
    a='12.09'
    b=a[0]
    print(b)

if __name__=='__main__':
    testtt()