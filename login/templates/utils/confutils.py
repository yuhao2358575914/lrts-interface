import os
import yaml
from login.templates.utils import getconf
from login.templates.utils.getconf import write_config_ini


def getApiName(apiname):
    """
    获取apiname
    :param apiname:
    :return:api路径
    """
    return getconf.get_global_conf('apinames', apiname)


def getAdminName(adminapiname):
    """
    获取adminapiname
    :param apiname:
    :return:adminapi路径
    """
    return getconf.get_global_conf('adminapis', adminapiname)


def getcurrentPath(currentPath):
    """
    获取currentPath
    :param apiname:
    :return:currentPath路径
    """
    return getconf.get_global_conf('currentPath', currentPath)


def get_private_key():
    """
    获取私钥
    :return:
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(path + '\\config\\private_key.pem') as pk:
        key_data = pk.read()
        return key_data


def get_public_key():
    """
    获取公钥钥
    :return:
    """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(path + '\\config\\public_key.pem') as pk:
        key_data = pk.read()
        return key_data


def init_configs(host_name):
    """
    环境配置初始化
    :param host_name:
    :return:
    """
    host_names = host_name.split(',')
    write_config_ini('HOST', 'apidomain', host_names[0])
    write_config_ini('HOST', 'admindomain', host_names[1])
    if 'earth' in host_name:
        write_config_ini('mysql', 'host', '172.16.6.2')
        write_config_ini('mysql', 'port', '3306')
        write_config_ini('mysql', 'username', 'readonly')
        write_config_ini('mysql', 'password', 'X7sMx68IOLNCk%)d#DZ!-=4E')
    elif 'moon' in host_name:
        write_config_ini('mysql', 'host', '172.16.7.2')
        write_config_ini('mysql', 'port', '3306')
        write_config_ini('mysql', 'username', 'lazyaudio')
        write_config_ini('mysql', 'password', 'q(nQ5_0xeYNriZaUSBvgP)@E')
    elif 'mars' in host_name:
        write_config_ini('mysql', 'host', '172.16.6.2')
        write_config_ini('mysql', 'port', '3306')
        write_config_ini('mysql', 'username', 'readonly')
        write_config_ini('mysql', 'password', 'X7sMx68IOLNCk%)d#DZ!-=4E')


def get_services_conf(key1, key2):
    """
    读取yaml文件获取配置，二级key
    :param key1:第一层级的key值
    :param key2:第二层级的key值
    :return:
    """
    config_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/service_config.yaml'
    f = open(config_path, 'r', encoding='utf-8')
    cfg = f.read()
    data = yaml.load(cfg)
    value = data[key1][key2]
    return value


def login_control():
    """
    获取登录开关配置
    :return:
    """
    return get_services_conf('keys', 'loginKey')
