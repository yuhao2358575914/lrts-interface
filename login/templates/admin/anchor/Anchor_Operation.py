"""
主播相关操作

"""

from json import loads

from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import dbutil, httputils
from login.templates.utils.confutils import getAdminName, getcurrentPath


def get_user_Type(user_id):
    """
    获取主播的type值
    :param user_id:
    :return: type
    """
    Type=dbutil.select('SELECT type FROM t_sns_partner WHERE  real_name IS NULL AND user_id='+str(user_id),'db_audiobook')
    if Type:
        return Type[0]["type"]
    else:
        return None


def get_user_address(user_id):
    """
    获取用户的地址
    :param user_id:
    :return:
    """
    number=user_id%10
    print(number)
    address_all= dbutil.select('SELECT address FROM t_user_ext_%s  WHERE user_id=%s'%(str(number),str(user_id)),
                         'db_audiobook')
    print('用户地址',address_all)
    if address_all[0]['address']:
        address=address_all[0]['address'][:3]
        subaddress=address_all[0]['address'][3:]
        if address[-1]=="0":
            address=address[:-1]
        return address,subaddress
    else:
        return 0
def get_recomLabel_value_according_to_feature(features):
    """
    根据features值获取recomLabel值
    :param features: features字段
    :return: recomLabel的值
    """
    list= features.split(';')  # key值字符串分割
    features_dict = {}
    for i in list:
        s = i.split('=')#字段用=分割
        features_dict[s[0]] = s[1]
    return features_dict['recomLabel']

def get_user_info_dict(user_id):
    """
    获取用户的信息，返回请求参数
    :param user_id: 用户ID
    :return:用户信息，字典类型
    """
    user_type=get_user_Type(user_id)
    params={"userId":str(user_id),"announcerType":str(user_type)}
    del params["announcerType"]#"announcerType"值不确认，删除该值
    r= httputils.getadmin(getAdminName("userExtGet.action"),
                          params,
                          login_admin(),
                          getcurrentPath('AnnouncerBookEdit'))
    rs=loads(r.text)
    print(rs)
    json_res={"userId":user_id}
    json_res["nickName"]=rs["data"]["encodeNickName"]
    json_res["jspFlag"] = "bookUser"#跟开发确认该字段是写死的
    json_res["areaIds"] = rs["data"]["areaIds"]
    json_res["copyrightAnnouncerId"] = rs["data"]["copyrightAnnouncerId"]
    json_res["copyrightAnnouncerName"] = rs["data"]["copyrightAnnouncerName"]
    if rs["data"]["unique"]=="True":
        json_res["isUnique"]="1"
    else:
        json_res["isUnique"]="0"
    features=rs["data"]['features']
    print('特性专职as12',features)
    if 'recomLabel' in features:
        json_res["recomLabel"]=get_recomLabel_value_according_to_feature(features)
    json_res["deadline"] = rs["data"]["deadline"]
    json_res["file"] = ""#该字段没有到为空
    json_res["email"] = rs["data"]["email"]
    json_res["sex"] = rs["data"]["sex"]
    address_all=get_user_address(user_id)#获取地址信息
    if address_all !=0:
        address=address_all[0]
        subaddress=address_all[1]
        json_res["address"] =address
        json_res["subAddress"] =subaddress
        json_res["description"] = rs["data"]["remark"]
    return json_res

def edit_user_info_by_dict(user_id, modifydatas):
    """
    编辑用户信息
    :param bookid: 主播id，为str，int也可以，代码做了处理
    :param modifydatas: 需要修改的字段，类型为dict，例如：{'desc':'中国当代仙侠小是书籍的数据22作'}
    :return:修改成功或失败信息
    """
    json_res = get_user_info_dict(user_id)
    for k, v in modifydatas.items():
        json_res[k] = v
    r = httputils.postadmin(getAdminName('userEdit.action'),
                            json_res,
                            login_admin(),
                            getcurrentPath('AnnouncerBookEdit'))
    res = loads(r.text)
    success_message = '编辑主播ID为%s信息:%s成功！' % (user_id,modifydatas)
    if res.get('status') == 0:
        print(success_message)
        return 0
    else:
        return res.get('msg')
