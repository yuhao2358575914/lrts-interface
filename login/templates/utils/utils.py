#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 15:59
# @Author  : caozhuo
# @FileName: utils.py
# @Software: PyCharm
# coding=utf-8
import datetime
import os
import random
import hashlib
import time

from datetime import timedelta

# 读取配置文件下sc安全码，分ios和安卓
from login.templates.utils import getconf

iosseccode = getconf.get_conf('securitycode', 'ios')
andseccode = getconf.get_conf('securitycode', 'andriod')


# 生成随机字符串
def ranstr(num):
    # 猜猜变量名为啥叫
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return str(salt)


# sc校验公共方法
def securitycode(apiname, parameters, type=1):
    keys = []
    for k, v in parameters.items():
        keys.append(k)
    keys.sort(reverse=False)
    urlpath = ''
    for key in keys:
        urlpath = urlpath + key + "=" + parameters[key] + "&"
        if (type == 1):
            initurl = apiname + '?' + urlpath.rstrip('&') + andseccode
        else:
            initurl = apiname + '?' + urlpath.rstrip('&') + iosseccode
    print(initurl)
    md5sc = hashlib.md5(initurl.encode("utf-8")).hexdigest()
    return md5sc


# 针对get方法返回拼接的参数串
def geturl(parameters):
    keys = []
    for k, v in parameters.items():
        keys.append(k)
    keys.sort(reverse=False)
    url = ''
    for key in keys:
        url = url + key + "=" + parameters[key] + "&"
    return url.rstrip('&')


# 校验某个key-vulue存在，返回True或Flase
global flag
flag = False


def jsoncomp(jdict, key, value):
    global flag
    if isinstance(jdict, list):
        for element in jdict:
            jsoncomp(element, key, value)
    elif isinstance(jdict, dict):
        if key in jdict.keys():
            if jdict[key] == value:
                try:
                    raise BaseException
                except BaseException as err:
                    print(err)
                    flag = True
                else:
                    jsoncomp(jdict[key], key, value)
        else:
            for x in jdict.keys():
                jsoncomp(jdict[x], key, value)
    return flag


# 根据key获取返回值value，当同一个key有多个时，可以返回多个value，以list方式返回
def get_json_value_by_key(in_json, target_key, results=[]):
    if isinstance(in_json, dict):
        for key in in_json.keys():
            data = in_json[key]
            get_json_value_by_key(data, target_key, results=results)
            if key == target_key:
                results.append(data)
    elif isinstance(in_json, list) or isinstance(in_json, tuple):
        for data in in_json:  # 循环当前列表
            get_json_value_by_key(data, target_key, results=results)
    for i in range(len(results)):
        if isinstance(results[i], dict):
            results.remove(results[i])
    return results


# 根据key获取返回value，不支持多个相同符合条件的value返回
def dict_get(dict1, objkey, default):
    tmp = dict1
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            if isinstance(v, dict):
                ret = dict_get(v, objkey, default)
                if ret is not default:
                    return ret
    return default


# 检查某个value在list下存在，若存在返回True，不存在返回False
def checklist(value, value_list):
    if isinstance(value_list, list):
        for i in range(len(value_list)):
            if value == value_list[i]:
                return True
        return False


def checklistValue_onlyOne_in_list(value_list, value_list_all):
    """
   传入两个list值，value_list中只有一个值在value_list_all则返回True

   """
    if isinstance(value_list, list):
        for i in value_list:
            if i in value_list_all:
                return True
        return False


def checklistValue_allIn_list(value_list, value_list_all):
    """
    传入两个list值，value_list中所有值在value_list_all则返回True

    """
    if isinstance(value_list, list):
        for i in value_list:
            if i not in value_list_all:
                return False
        return True


# 生成随机手机号
def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]
    # 最后八位数字
    suffix = random.randint(9999999, 100000000)
    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


def check_keyword_in_list(keyword, list=[]):
    '''根据keyword值，判断keyword是否在包含在列表的值中'''
    if list:
        # 如果不为空继续判断，否则返回False
        if keyword in list:
            # 精确搜索，keyword就是list的某个值，则返回成功
            # 如：keyword='仙逆'，list=['仙是什么','仙逆']
            return True
        else:
            # 模糊搜索,第一个name值中包含关键字，则断言成功，否则失败
            # 如：keyword='仙逆'，list=['仙是什么','仙逆1111','我是仙逆']
            j = 0
            for i in range(len(list)):
                if keyword in list[i]:
                    return True
                else:
                    j = j + 1
                    if j == len(list):
                        return False
    else:
        return False


def check_target_key_value(key1, key2, value1, value2, reslist):
    '''根据目标key遍历value跟目标value比较'''
    if isinstance(reslist, list):
        for i in range(len(reslist)):
            if str(reslist[i].get(key1)) == value1 and str(reslist[i].get(key2)) == value2:
                return 1


def get_local_time_day(n=0):
    '''获取当前时间/当前时间往后延N天的时间'''
    return (datetime.datetime.now() + datetime.timedelta(days=n)).strftime("%Y-%m-%d %H:%M:%S")


def get_local_time_second(n=0):
    '''获取当前时间/当前时间往后延N秒的时间'''
    return (datetime.datetime.now() + datetime.timedelta(seconds=n)).strftime("%Y-%m-%d %H:%M:%S")


def get_local_time_second_new(n=0):
    '''获取当前时间/当前时间往后延N秒的时间'''
    return str((datetime.datetime.now() + datetime.timedelta(seconds=n)).strftime("%Y%m%d%H%M%S"))


def get_local_time_str():
    '''获取当前时间的时间戳精确到毫秒'''
    return str(int(round(time.time() * 1000)))


def del_dict_key_value_by_list(dict_data, keylist):
    '''
    删除dict_data下多个key对应的数据
    :param dict_data:
    :param keylist:
    :return:
    '''
    if isinstance(keylist, list) and isinstance(dict_data, dict):
        for i in range(len(keylist)):
            dict_data.pop(keylist[i])
        return dict_data
    else:
        return '入参格式错误，请检查'


def dec_To_Bin(num):
    """
    十进制转二进制并返回8位
    :param num:待转换正整数，int类型
    :return: 返回8位不足则补0
    """
    sts = bin(num).replace('0b', '')
    oss = ''
    if len(sts) < 8:
        for i in range(8 - len(sts)):
            oss = '0' + oss
        bins = oss + sts
        return bins[::-1]
    else:
        return sts[::-1]

def getFiles(path, suffix):
    """
    根据路径查找对应文件是否存在
    :param path: 查找目录
    :param suffix: 关键字
    :return:满足条件的文件地址列表
    """
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]
