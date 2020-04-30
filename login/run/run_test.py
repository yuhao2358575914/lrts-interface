#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 10:08
# @Author  : caozhuo
# @FileName: run_test.py
# @Software: PyCharm
import os
import unittest
from BeautifulReport import BeautifulReport

from login.templates.utils.utils import get_local_time_second_new


def run_test_bf_old(patterns, exec_type='batch'):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    suite_tests = unittest.defaultTestLoader.discover(path + "/testcases",
                                                      pattern=patterns,
                                                      top_level_dir=path)  # "./cases"表示当前目录，"case*.py"匹配当前目录下所有tests.py结尾的用例
    if exec_type == 'batch':
        file_name = 'test_report' + get_local_time_second_new()
        BeautifulReport(suite_tests).report(filename=file_name,
                                            description='懒人听书接口测试',
                                            report_dir=path + '/templates/login/reports')  # log_path='.'把report放到当前目录下
        return file_name
    else:
        file_name = 'test_report' + exec_type + '_' + get_local_time_second_new()
        BeautifulReport(suite_tests).report(filename=file_name,
                                            description='懒人听书接口测试',
                                            report_dir=path + '/templates/login/reports/single')  # log_path='.'把report放到当前目录下
        return file_name


def run_test_bf(patterns):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    suite_tests = unittest.defaultTestLoader.discover(path + "/testcases",
                                                      pattern=patterns,
                                                      top_level_dir=path)  # "./cases"表示当前目录，"case*.py"匹配当前目录下所有tests.py结尾的用例
    return suite_tests


def reporter(suite_tests):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BeautifulReport(suite_tests).report(filename='test_report',
                                        description='懒人听书接口测试',
                                        report_dir=path + '/templates/login')  # log_path='.'把report放到当前目录下