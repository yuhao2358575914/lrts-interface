import json

from login.templates.users.Get_UserInfo_By_Token import get_user_isVip
from login.templates.users.User import get_auto_register_token_app
from login.templates.utils import httputils
from login.templates.utils.confutils import getApiName


def get_entity_price_by_id(entityId: int, entityType: str) -> object:
    """
    获取资源价格信息
    :param entityId:资源id
    :param entityType:资源类型resourceType，参考constant.py文件
    :return:返回的priceType，1整本 2按章收费
    """
    data = {'entityId': str(entityId), 'entityType': entityType, 'token': get_auto_register_token_app()}
    r = httputils.get_app(getApiName('entityPrice'), data)
    print(r.text)
    dict_res = {'priceType': str(json.loads(r.text)['priceType']), 'price': str(json.loads(r.text)['price'])}
    discounts = []
    for i in range(len(json.loads(r.text)['discounts'])):
        discounts.append((json.loads(r.text)['discounts'][i]['id']))
    dict_res['discounts'] = discounts
    return dict_res


def get_entity_price_totalFee(entityId: str, entityType: str, token):
    data = {'entityId': str(entityId), 'entityType': entityType, 'token': get_auto_register_token_app()}
    r = httputils.get_app(getApiName('entityPrice'), data)
    print('价格信息为：', r.text)
    # if entityType == '1':
    #     price = float(json.loads(r.text)['discountPrice'])
    # elif entityType == '2':
    price = float(json.loads(r.text)['price'])
    discounts = json.loads(r.text)['discounts']
    discountRate = float(0)
    for i in range(len(discounts)):
        if discounts[i].get('type') == 1:
            discountRate = float(discounts[i].get('value'))
        else:
            discountRate = 1
    if get_user_isVip(token) == 1:
        totalFee = price * discountRate
    else:
        totalFee = price
    fee = str(round(totalFee))[:-1]
    return fee
