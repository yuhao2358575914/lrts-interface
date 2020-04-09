import json

from json import loads

from login.templates.admin.account.adminlogin import login_admin
from login.templates.utils import httputils
from login.templates.utils.confutils import getAdminName, getcurrentPath, getApiName
from login.templates.utils.utils import dec_To_Bin


def get_album_info_dict(album_id):
    """
    获取节目信息
    :param album_id:书籍id，str格式
    :return: 返回书籍信息
    """
    r = httputils.getadmin(getAdminName('albumInfo.action'),
                           {'id': album_id},
                           login_admin(),
                           getcurrentPath('AlbumEdit'))
    res = loads(r.text)
    json_res = {}
    json_res["id"] = album_id
    json_res["userId"] = res["data"]["userId"]
    json_res["subTypeId"] = ""  # 暂时不知道字段代表意思
    json_res["name"] = res["data"]["name"]
    json_res["description"] = res["data"]["description"]
    json_res["reason"] = res["data"]["reason"]
    json_res["shortReason"] = res["data"]["shortReason"]
    json_res["source"] = res["data"]["source"]
    json_res["fatherId"] = res["data"]["fatherId"]
    json_res["typeId"] = res["data"]["typeId"]
    json_res["announcer"] = res["data"]["announcer"]
    json_res["audioCount"] = res["data"]["audioCount"]
    json_res["estimatedSections"] = res["data"]["estimatedSections"]
    json_res["audioQuality"] = res["data"]["audioQuality"]
    json_res["rating"] = res["data"]["rating"]
    json_res["sort"] = res["data"]["sort"]
    json_res["contentState"] = res["data"]["contentState"]
    json_res["interruptUpdate"] = res["data"]["interruptUpdate"]
    json_res["playsShow"] = res["data"]["playsShow"]
    json_res["downsShow"] = res["data"]["downloadsShow"]
    json_res["payFree"] = res["data"]["payFree"]
    json_res["operationTag"] = res["data"]["operationTag"]
    json_res["tagDeadlineTime"] = res["data"]["tagDeadlineTime"]

    if res["data"]["remark"] is None:
        json_res["remark"] = ""
    else:
        json_res["remark"] = res["data"]["remark"]
    censor_flag = res.get('data').get('censorFlag')
    bin_code = dec_To_Bin(censor_flag)
    if bin_code[0] == '0':
        json_res['canNotSearch'] = 'true'
    if bin_code[1] == '0':
        json_res['canNotFuzzySearch'] = 'true'
    if bin_code[2] == '0':
        json_res['canNotRecommendByMen'] = 'true'
    if bin_code[3] == '0':
        json_res['canNotRecommendByAlgorithm'] = 'true'
    if bin_code[4] == '0':
        json_res['canNotImportantShow'] = 'true'
    if bin_code[5] == '0':
        json_res['canNotFreeSection'] = 'true'
    if bin_code[6] == '0':
        json_res['canNotBuySection'] = 'true'
    if bin_code[7] == '0':
        json_res['canNotUnBuySection'] = 'true'
    json_res["contentLevel"] = res["data"]["contentLevel"]
    json_res["contentLevelDesc"] = res["data"]["contentLevelDesc"]
    json_res["cover"] = res["data"]["cover"]
    json_res["rename"] = ""  # 不知道什么字段，暂为空，重命名？
    json_res["coverFormat"] = "album_cover"  # 应该是写死的
    json_res["file"] = ""  # 不知道什么字段，为空
    json_res["coverFileUrl"] = res["data"]["coverFileUrl"]
    json_res["fileId"] = res["data"]["coverFile"]
    json_res["rename1"] = ""  # 不知道什么字段，暂为空
    json_res["coverFormat2"] = "new_album_cover"  # 应该是写死的
    json_res["editType"] = "1"  # 屏蔽是2，修改是1
    json_res["userIds"] = res["data"]["userId"]
    return json_res


def edit_album_info_by_dict(album_id, modifydatas):
    """
    编辑节目信息
    :param album_id: 节目id，为str
    :param modifydatas: 需要修改的字段，类型为dict，例如：{'desc':'中国当代仙侠小是书籍的数据22作'}
    :return:修改成功或失败信息
    """
    json_res = get_album_info_dict(album_id)
    for k, v in modifydatas.items():
        json_res[k] = v
    r = httputils.postadmin(getAdminName("albumEdit.action"),
                            json_res,
                            login_admin(),
                            getcurrentPath('AlbumEdit'))
    res = loads(r.text)
    success_message = '编辑节目:%s信息:%s成功！' % (album_id, modifydatas)
    if res.get('status') == 0:
        print(success_message)
        return 0
    else:
        return res.get('msg')


def get_albumn_chapters(token: str, ablumn_Id: str):
    """
    分开返回节目已购及未购章节
    :param token: app用户token
    :param ablumn_Id:节目id
    :return:返回章节是否已购，buy-已购 unbuy-未购
    """
    r = httputils.get_app(getApiName('getAblumnAudios'),
                          {'ablumnId': ablumn_Id, 'token': token, 'pageSize': '10000', 'pageNum': '1', 'sortType': '0'}
                          )
    result = json.loads(r.text)
    res_list = result['list']
    return_list_1 = []
    return_list_0 = []
    for res in res_list:
        if res['buy'] == 1:
            return_list_1.append(res['audioId'])
        elif res['buy'] == 0:
            return_list_0.append(res['audioId'])
    return {'buy': return_list_1, 'unbuy': return_list_0}
