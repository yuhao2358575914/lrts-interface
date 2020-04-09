#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 10:08
# @Author  : caozhuo
# @FileName: run_test.py
# @Software: PyCharm
import os
import unittest
from BeautifulReport import BeautifulReport


def run_test_bf_old(patterns):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    suite_tests = unittest.defaultTestLoader.discover(path + "/testcases",
                                                      pattern=patterns,
                                                      top_level_dir=path)  # "./cases"表示当前目录，"case*.py"匹配当前目录下所有tests.py结尾的用例
    BeautifulReport(suite_tests).report(filename='test_report',
                                        description='懒人听书接口测试',
                                        report_dir=path + '/templates/login')  # log_path='.'把report放到当前目录下


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
# list1 = ['Case_Search_Normal_Word.py', 'case_Book_Free_Chapters_For_Purchased_Users_Not.py','Case_Search_Special_Character.py']
# suite = unittest.TestSuite()
# for i in list1:
#     suite_tests=run_test_bf(i)
#     suite.addTests(suite_tests)
# reporter(suite)
