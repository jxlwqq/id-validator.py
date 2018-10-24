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
