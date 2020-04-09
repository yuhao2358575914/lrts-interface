# -*- coding: utf-8 -*-
# @Author  : caozhuo
# @File    : Config.py

from configparser import ConfigParser
import os
class Config:
    def get_conf(title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        config = ConfigParser()
        # conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '\config\config.ini')
        conf_path=os.path.dirname(os.path.abspath(__file__))+'\config'
        print('**************************')
        print(conf_path)
        if not os.path.exists(conf_path):
            raise FileNotFoundError("请确保配置文件存在！")
        config.read(conf_path+'/config.ini', encoding='utf-8')
        return config.get(title, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
