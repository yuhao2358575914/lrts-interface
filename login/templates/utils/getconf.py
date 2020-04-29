# coding=utf-8
import configparser

from gevent import os


def get_conf(title: str, value: str) -> object:
    '''
        获取可变配置，读取config.ini下的数据
        :param title:
        :param value:
        :return:
        '''
    config = configparser.RawConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config.ini', encoding='utf-8')
    cf = config.get(title, value)
    if cf:
        return cf
    else:
        return None


def get_global_conf(title, value):
    '''
        获取通用配置，读取config_global.ini下的数据
        :param title:
        :param value:
        :return:
        '''
    config = configparser.RawConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config_global.ini', encoding='utf-8')
    cf = config.get(title, value)
    return cf


def getdict(title, key):
    '''
        获取通用配置以字典格式返回，读取config.ini下的数据
        :param title:
        :param key:
        :return:
        '''
    config = configparser.RawConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config.ini', encoding='utf-8')
    value = config.get(title, key)
    dic = {key: value}
    return dic


def get_dict_all(title):
    '''
        根据title获取通用配置以字典格式返回
        :param title:
        :param key:
        :return:
        '''
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config.ini', encoding='utf-8')
    dicts = {}
    for key in config.options(title):
        dicts = {**dicts, **getdict(title, key)}
    return {title: dicts}


def get_config_info():
    """
    获取配置信息
    :return:
    """
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config.ini', encoding='utf-8')
    res_dict = {}
    for section in config.sections():
        res_dict = {**res_dict, **get_dict_all(section)}
    return res_dict


def write_config_ini(title, key, value):
    config = configparser.RawConfigParser()
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config.read(path + '/config/config.ini', encoding='utf-8')
    config.set(title, key, value)
    config.write(open(path + '/config/config.ini', "w", encoding="utf-8"))
