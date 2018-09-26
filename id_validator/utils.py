#!/usr/bin/env python
# encoding: utf-8

import functools
import datetime


def check_for_none(func):
    """
    检测是否是 None
    :param func:
    :return:
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] is None:
            return False
        return func(*args, **kwargs)

    return decorator


def check_empty_string(func):
    """
    检测是否是空字符串
    :param func:
    :return:
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) == 0:
            return False
        return func(*args, **kwargs)

    return decorator


def check_id_card_length(func):
    """
    检测身份证号码长度
    :param func:
    :return:
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) != 15 and len(args[0]) != 18:
            return False
        return func(*args, **kwargs)

    return decorator


def check_date(m, d, y):
    """
    检测日期
    :param m:
    :param d:
    :param y:
    :return:
    """
    try:
        m, d, y = map(int, (m, d, y))
        datetime.date(y, m, d)
        return True
    except ValueError:
        return False


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
        x = length - len(string)
        for i in range(0, x):
            if right:
                string = string + character
            else:
                string = character + string
        return string


def is_set(variable):
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
