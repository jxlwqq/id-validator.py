#!/usr/bin/env python
# encoding: utf-8

import datetime


def get_str_pad(string, length=2, character='0', right=False):
    """
    字符串填充
    :param string:
    :param length:
    :param character:
    :param right:
    :return:
    """
    string = str(string)
    character = str(character)
    if len(string) >= length:
        return string
    else:
        frequency = length - len(string)
        if right:
            string = string + character * frequency
        else:
            string = character * frequency + string
        return string


def is_set(variable):
    """
    变量是否定义
    :param variable:
    :return:
    """
    return variable in locals() or variable in globals()


def str_to_time(string, format_string="%Y-%m-%d"):
    """
    将字符串格式转换为日期格式
    :param string:
    :param format_string:
    :return:
    """
    import time
    str_time = time.strptime(string, format_string)
    return int(time.mktime(str_time))


def check_year(year):
    """
    检测年份
    :param year:
    :return:
    """
    return False if year == '' or year < '1800' or year > str(datetime.datetime.now().year) else True


def check_month(month):
    """
    检测月份
    :param month:
    :return:
    """
    return False if month == '' or month == '00' or month > '12' else True


def check_day(day):
    """
    检测日期
    :param day:
    :return:
    """
    return False if day == '' or day == '00' or day > '31' else True
