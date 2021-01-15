#!/usr/bin/env python
# encoding: utf-8

import re
import random
import datetime
from . import data
from . import func


def generator_address_code(address=None):
    """
    生成地址码
    :param address:
    :return:
    """
    address_code = ''
    if address is not None:
        for key, val in data.get_address_code().items():
            if val == address:
                address_code = key
                break

    if address_code != '' and address_code[0:1] == '8':
        return address_code

    if address_code != '':
        if address_code[2:6] == '0000':
            province_code = address_code[0:2]
            pattern = r'^%s\d{2}(?!00)[0-9]{2}$' % province_code
            address_code = get_random_address_code(pattern)

        if address_code[4:6] == '00':
            city_code = address_code[0:4]
            pattern = r'^%s(?!00)[0-9]{2}$' % city_code
            address_code = get_random_address_code(pattern)

    else:
        pattern = r'^\d{4}(?!00)[0-9]{2}$'
        address_code = get_random_address_code(pattern)

    return address_code


def generator_birthday_code(address_code, address, birthday=None):
    """
    生成出生日期码
    :param birthday:
    :return:
    """
    year = ''
    month = ''
    day = ''
    start_year = 0
    end_year = 9999

    if birthday is not None:
        year = func.get_str_pad(birthday[0:4], 4)
        month = func.get_str_pad(birthday[4:6], 2)
        day = func.get_str_pad(birthday[6:8], 2)

    if not func.check_year(year):
        year = '19' + str(random.randint(50, 99))

    address_code_timeline = data.get_address_code_timeline()
    timeline = address_code_timeline.get(address_code, '')
    if timeline != '':
        for key, val in enumerate(timeline):
            if val['address'] == address:
                start_year = start_year if val['start_year'] == '' else val['start_year']
                end_year = end_year if val['end_year'] == '' else val['end_year']

    if year < str(start_year):
        year = str(start_year)

    if year > str(end_year):
        year = str(end_year)

    if not func.check_month(month):
        month = func.get_str_pad(random.randint(1, 12))

    if not func.check_day(day):
        day = func.get_str_pad(random.randint(1, 28))

    if not check_birthday_code(year + month + day):
        year = str(random.randint(max(1950, start_year), min(end_year, datetime.datetime.now().year) - 1))
        month = func.get_str_pad(random.randint(1, 12))
        day = func.get_str_pad(random.randint(1, 28))

    return year + month + day


def generator_order_code(sex=None):
    """
    生成顺序码
    :param sex:
    :return:
    """
    order_code = random.randint(101, 999)
    if sex is not None and int(sex) != order_code % 2:
        order_code -= 1
    return str(order_code)


def generator_check_bit(body):
    """
    生成校验码
    :param body:
    :return:
    """
    pos_weight = {}
    weight_list = range(2, 19)[::-1]
    for i in weight_list:
        weight = pow(2, i - 1) % 11
        pos_weight[i] = weight

    body_sum = 0
    body_list = list(body)
    count = len(body)

    for j in range(count):
        body_sum += int(body_list[j], 10) * pos_weight[18 - j]

    check_bit = (12 - (body_sum % 11)) % 11

    if check_bit == 10:
        check_bit = 'X'

    return str(check_bit)


def check_address_code(address_code, birthday_code):
    """
    检测地址码
    :param address_code:
    :param birthday_code:
    :return:
    """
    address_info = get_address_info(address_code, birthday_code)
    if address_info['province'] == '':
        return False
    return True


def check_birthday_code(birthday_code):
    """
    检测日期
    :param birthday_code:
    :return:
    """

    if birthday_code is None or birthday_code == '' or len(birthday_code) != 8:
        return False

    year = func.get_str_pad(birthday_code[0:4], 4)
    month = func.get_str_pad(birthday_code[4:6], 2)
    day = func.get_str_pad(birthday_code[6:8], 2)

    if not func.check_year(year):
        return False

    if not func.check_month(month):
        return False

    if not func.check_day(day):
        return False

    try:
        month, day, year = map(int, (month, day, year))
        datetime.date(year, month, day)
        return True
    except ValueError:
        return False


def check_order_code(order_code):
    """
    检测顺序码
    :param order_code:
    :return:
    """
    if len(order_code) != 3:
        return False
    return True


def check_abandoned(address_code):
    """
    检测地址码是否废弃
    :param address_code:
    :return:
    """
    return 0 if data.get_address_code().get(address_code, 0) else 1


def get_id_argument(id_card):
    """
    获取身份证号码信息
    :param id_card:
    :return:
    """
    id_card = id_card.upper()
    id_length = len(id_card)
    if id_length == 18:
        code = {
            'body': id_card[0:17],
            'address_code': id_card[0:6],
            'birthday_code': id_card[6:14],
            'order_code': id_card[14:17],
            'check_bit': id_card[17:18],
            'type': 18
        }
    else:
        code = {
            'body': id_card,
            'address_code': id_card[0:6],
            'birthday_code': '19' + id_card[6:12],
            'order_code': id_card[12:15],
            'check_bit': '',
            'type': 15
        }
    return code


def get_address_info(address_code, birthday_code):
    """
    获取地址信息
    :param address_code:
    :param birthday_code:
    :return:
    """
    address_info = {}
    first_character = address_code[0:1]  # 用于判断是否是港澳台居民居住证（8字开头）

    province_address_code = address_code[0:2] + '0000'
    city_address_code = address_code[0:4] + '00'

    address_info['province'] = get_address(province_address_code, birthday_code)

    if first_character != '8':
        address_info['city'] = get_address(city_address_code, birthday_code)
        address_info['district'] = get_address(address_code, birthday_code)
    else:
        address_info['city'] = ''
        address_info['district'] = ''

    return address_info


def get_address(address_code, birthday_code):
    """
    通过地址码与出生日期码获取地址信息
    :param address_code:
    :param birthday_code:
    :return:
    """
    address = ''
    address_code_timeline = data.get_address_code_timeline()
    timeline = address_code_timeline.get(address_code, '')
    if timeline != '':
        year = int(birthday_code[0:4])
        for key, val in enumerate(timeline):
            start_year = 0 if val['start_year'] == '' else val['start_year']
            end_year = 9999 if val['end_year'] == '' else val['end_year']
            if end_year >= year >= start_year:
                address = val['address']

    return address


def get_constellation(birthday_code):
    """
    获取星座信息
    :param birthday_code:
    :return:
    """
    month = int(birthday_code[4:6])
    day = int(birthday_code[6:8])

    start_date = data.get_constellation()[month]['start_date']
    start_day = int(start_date.split('-')[-1])

    if day < start_day:
        tmp_month = 12 if month - 1 == 0 else month - 1
        return data.get_constellation()[tmp_month]['name']

    return data.get_constellation()[month]['name']


def get_chinese_zodiac(birthday_code):
    """
    获取生肖
    :param birthday_code:
    :return:
    """
    start = 1900  # 子鼠
    end = int(birthday_code[0:4])
    key = (end - start) % 12
    return data.get_chinese_zodiac()[key]


def get_random_address_code(pattern):
    """
    获取随机地址码
    :param pattern:
    :return:
    """
    pattern = re.compile(pattern)
    result = []
    for key in data.get_address_code().keys():
        if re.match(pattern, key):
            result.append(key)
    return result[random.choice(range(len(result)))]
