"""
书籍相关操作

"""
import json
import random

from login.templates.admin.account.adminlogin import login_admin
from login.templates.users.Get_UserInfo_By_Token import get_userid_by_token
from login.templates.utils import dbutil, httputils
from login.templates.utils.confutils import getAdminName, getcurrentPath
from login.templates.utils.utils import dec_To_Bin

"""
获取书籍的免费章节
"""


def operation_book_get_freecharpters(bookid):
    res = dbutil.select('SELECT t.`free_sections`  FROM audiobook.`t_book` t WHERE t.book_id=' + bookid, 'db_audiobook')
    rlt = str(res[0].get('free_sections'))
    if ',' in rlt:
        freelist = rlt.split(',')
        outlist = []
        for i in range(len(freelist)):
            if '-' in freelist[i]:
                outlist.append(freelist[i])
                start = freelist[i][:freelist[i].index('-')]
                end = freelist[i][freelist[i].index('-') + 1:]
                for j in range(int(end) - int(start) + 1):
                    k = int(start) + j
                    freelist.append(str(k))
                    endlist = list(set(freelist) - set(outlist))
                    endlist.sort()
        return endlist
    elif '-' in rlt:
        freelist1 = []
        strt = rlt[:rlt.index('-')]
        ed = rlt[rlt.index('-') + 1:]
        for m in range(int(ed) - int(strt) + 1):
            k1 = int(strt) + m
            freelist1.append(str(k1))
            freelist1.sort()
        return freelist1
    else:
        return str(res[0].get('free_sections'))


"""
获取某个用户已购书籍的已购章节，返回首个已购章节
"""


def operation_book_get_buyedcharpters(bookid, token):
    res = dbutil.select(
        'SELECT item_ids FROM t_consume WHERE user_id =' + str(get_userid_by_token(token)) + ' AND goods_id=' + bookid,
        'db_audiobook')
    rlt = str(res[0].get('item_ids'))
    if '-' in str(res[0].get('item_ids')):
        if ',' in rlt[:rlt.index('-')]:
            return rlt[:rlt.index(',')]
        else:
            return rlt[:rlt.index('-')]
    elif ',' in str(res[0].get('item_ids')):
        if '-' in rlt[:rlt.index(',')]:
            return rlt[:rlt.index('-')]
        else:
            return rlt[:rlt.index(',')]
    else:
        return str(res[0].get('item_ids'))


"""
获取某个用户已购书籍的已购章节，以list返回所有已购章节
"""


# str(get_userid_by_token(token))
def operation_book_get_buyedcharpters_all(bookid, token):
    res = dbutil.select(
        'SELECT item_ids FROM t_consume WHERE user_id =' + str(get_userid_by_token(token)) + ' AND goods_id=' + bookid,
        'db_audiobook')
    if res:
        rlt = str(res[0].get('item_ids'))
    else:
        return []
    if ',' in rlt:
        chargelist = rlt.split(',')
        outlist = []
        for i in range(len(chargelist)):
            if '-' in chargelist[i]:
                outlist.append(chargelist[i])
                start = chargelist[i][:chargelist[i].index('-')]
                end = chargelist[i][chargelist[i].index('-') + 1:]
                for j in range(int(end) - int(start) + 1):
                    k = int(start) + j
                    chargelist.append(str(k))
                    endlist = list(set(chargelist) - set(outlist))
                    endlist.sort()
        return endlist
    elif '-' in rlt:
        chargelist1 = []
        strt = rlt[:rlt.index('-')]
        ed = rlt[rlt.index('-') + 1:]
        for m in range(int(ed) - int(strt) + 1):
            k1 = int(strt) + m
            chargelist1.append(k1)
            chargelist1.sort()
        return chargelist1
    else:
        return str(res[0].get('item_ids'))


"""
获取某个用户已购书籍的未购章节，以list返回所有未购章节
"""


def operation_book_get_unbuyedcharpters_all(bookid, token):
    sectioncount = dbutil.select('SELECT t.`section` FROM audiobook.`t_book` t  WHERE t.`book_id`=' + bookid,
                                 'db_audiobook')
    sct = sectioncount[0].get('section')
    all_list = []
    for i in range(sct):
        all_list.append(str(i + 1))
    print('所有章节:', all_list)
    re_list = list(set(all_list) - set(operation_book_get_buyedcharpters_all(bookid, token)) - set(
        operation_book_get_freecharpters(bookid)))
    re_list.sort()
    msg = 'no section'
    if re_list:
        return re_list
    else:
        return msg


def get_book_by_pay_type(paytype, count):
    """
    根据pay_type获取N本在线书籍
    :param paytype:付款类型,参考constant.py
    :param count:获取书籍本数
    :return:
    """
    startint = 10 + int(90 * random.random())
    res = dbutil.select(
        'SELECT book_id FROM t_book WHERE pay_type=%d AND bState=0 LIMIT %d,%d' % (paytype, startint, count),
        'db_audiobook')
    books = ''
    for i in range(len(res)):
        k = str(res[i].get('book_id'))
        books += ',%s' % k
    return books.lstrip(',')


def get_albumn_by_pay_type(paytype, count):
    """
    根据pay_type获取N个在线节目
    :param paytype:付款类型,参考constant.py
    :param count:获取书籍本数
    :return:
    """
    res = dbutil.select(
        'SELECT id FROM t_sns_ablumn WHERE pay_type=%d AND status=0 LIMIT 1,%d' % (paytype, int(count)),
        'db_audiobook')
    books = ''
    for i in range(len(res)):
        k = str(res[i].get('id'))
        books += ',%s' % k
    return books.lstrip(',')


def get_read_book_charge(count: int):
    """
    获取付费的阅读书籍
    :type count: int
    :param count: 本数
    :return:
    """
    res = dbutil.select(
        'SELECT id FROM t_read_book WHERE pay_type=1 AND state=1 LIMIT 1,%d' % count,
        'db_audiobook')
    books = ''
    for i in range(len(res)):
        k = str(res[i].get('id'))
        books += ',%s' % k
    return books.lstrip(',')


def get_book_info_dict(bookid):
    """
    获取书籍信息
    :param bookid:书籍id，str格式
    :return: 返回书籍信息
    """
    r = httputils.getadmin(getAdminName('bookInfo'),
                           {'bookId': bookid},
                           login_admin(),
                           getcurrentPath('BookAdd'))
    json_data = json.loads(r.text)
    if '书籍不存在' not in json_data:
        json_res = {'bookId': bookid}
        json_res['bookName'] = json_data.get('data').get('bookName')
        json_res['fatherTypeId'] = json_data.get('data').get('fatherTypeId')
        json_res['sonTypeId'] = json_data.get('data').get('sonTypeId')
        if json_data.get('data').get('announcerList'):
            size = len(json_data.get('data').get('announcerList'))
            json_res['userId'] = json_data.get('data').get('announcerList')[size - 1].get('userId')
        json_res['sections'] = json_data.get('data').get('sections')
        json_res['estimatedSections'] = json_data.get('data').get('estimatedSections')
        json_res['audioQuality'] = json_data.get('data').get('audioQuality')
        json_res['length'] = json_data.get('data').get('length')
        json_res['sort'] = json_data.get('data').get('sort')
        json_res['state'] = json_data.get('data').get('state')
        json_res['interruptUpdate'] = json_data.get('data').get('interruptUpdate')
        json_res['payFree'] = json_data.get('data').get('payFree')
        json_res['operationTag'] = json_data.get('data').get('operationTag')
        json_res['priorityType'] = '-1'
        json_res['bState'] = json_data.get('data').get('bState')
        json_res['stateReason'] = json_data.get('data').get('stateReason')
        json_res['desc'] = json_data.get('data').get('desc')
        json_res['rating'] = json_data.get('data').get('rating')
        json_res['recommendReason'] = json_data.get('data').get('recReason')
        json_res['shortRecReason'] = json_data.get('data').get('shortRecReason')
        json_res['contentLevel'] = json_data.get('data').get('contentLevel')
        json_res['contentLevelDesc'] = json_data.get('data').get('contentLevelDesc')
        json_res['downloads'] = json_data.get('data').get('downloads')
        json_res['downsShow'] = json_data.get('data').get('downsShow')
        json_res['plays'] = json_data.get('data').get('plays')
        json_res['playsShow'] = json_data.get('data').get('playsShow')
        json_res['commentMeanFactor'] = '0'
        json_res['cover'] = json_data.get('data').get('cover')
        json_res['coverFormat'] = 'book_cover'
        json_res['labelIds'] = json_data.get('data').get('labels')
        censor_flag = json_data.get('data').get('censorFlag')
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
        announcer_list = json_data.get("data").get('announcerList')
        user_ids = []
        for i in range(len(announcer_list)):
            user_ids.append(announcer_list[i].get('userId'))
        json_res['userIds'] = str(user_ids)
        print(json_res)
        return json_res


def edit_book_info_by_dict(bookid, modifydatas):
    """
    编辑书籍信息
    :param bookid: 书籍id，为str
    :param modifydatas: 需要修改的字段，类型为dict，例如：{'desc':'中国当代仙侠小是书籍的数据22作'}
    :return:修改成功或失败信息
    """
    json_res = get_book_info_dict(bookid)
    for k, v in modifydatas.items():
        json_res[k] = v
    r = httputils.postadmin(getAdminName('BookEdit'),
                            json_res,
                            login_admin(),
                            getcurrentPath('BookAdd'))
    res = json.loads(r.text)
    success_message = '编辑书籍:%s信息:%s成功！' % (bookid, modifydatas)
    if res.get('status') == 0:
        print(success_message)
        return 0
    else:
        return res.get('msg')


def edit_book_info_approve(bookid):
    """
    审核书籍
    :param bookid:类型为str
    :return:
    """
    bState = get_book_info_dict(bookid).get('bState')
    if bState == 2:
        r = httputils.postadmin(getAdminName('bookApprove'),
                                {'bookId': bookid},
                                login_admin(),
                                getcurrentPath('bookList'))
        json_res = json.loads(r.text)
        res_approve = json_res.get('status')
        if res_approve == 0:
            return '书籍：%s审核通过！' % bookid
        else:
            print(json_res.get('msg'))
            return json_res.get('msg')
    else:
        return '书籍：%s状态不正确，无法审核！' % bookid


def push_a_book_To_online(bookid):
    """
    将一本书籍上线
    :param bookid:类型为str
    :return:
    """
    bState = get_book_info_dict(bookid).get('bState')
    if bState == 2:
        edit_book_info_approve(bookid)
    elif bState == 1:
        msg = edit_book_info_by_dict(bookid, {'bState': '2'})
        if msg == 0:
            edit_book_info_approve(bookid)
    elif bState == 0:
        return '书籍%s已经是在线状态啦！' % bookid
