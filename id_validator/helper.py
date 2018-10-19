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


def generator_birthday_code(birthday=None):
    """
    生成出生日期码
    :param birthday:
    :return:
    """
    year = ''
    month = ''
    day = ''

    if birthday is not None:
        year = func.get_str_pad(birthday[0:4], 4)
        month = func.get_str_pad(birthday[4:6], 2)
        day = func.get_str_pad(birthday[6:8], 2)

    if not func.check_year(year):
        year = '19' + str(random.randint(50, 100))

    if not func.check_month(month):
        month = func.get_str_pad(random.randint(1, 12))

    if not func.check_day(day):
        day = func.get_str_pad(random.randint(1, 28))

    if not check_birthday_code(year + month + day):
        year = '19' + str(random.randint(50, 100))
        month = func.get_str_pad(random.randint(1, 12))
        day = func.get_str_pad(random.randint(1, 28))

    return year + month + day


def generator_order_code(sex=None):
    """
    生成顺序码
    :param sex:
    :return:
    """
    order_code = random.randint(101, 1000)
    if sex == 1:
        order_code = order_code - 1 if order_code % 2 == 0 else order_code
    if sex == 0:
        order_code = order_code if order_code % 2 == 0 else order_code - 1
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


def check_address_code(address_code):
    """
    检测地址码
    :param address_code:
    :return:
    """
    address_info = get_address_info(address_code)
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


def get_address_info(address_code):
    """
    获取地址信息
    :param address_code:
    :return:
    """
    address_info = {}
    first_character = address_code[0:1]  # 用于判断是否是港澳台居民居住证（8字开头）

    province_address_code = address_code[0:2] + '0000'
    city_address_code = address_code[0:4] + '00'

    address_code_dist = data.get_address_code()
    abandoned_address_code_dist = data.get_abandoned_address_code()
    address_info['province'] = address_code_dist.get(province_address_code, '')

    if address_info['province'] == '':
        address_info['province'] = abandoned_address_code_dist.get(province_address_code, '')

    if first_character != '8':
        address_info['city'] = address_code_dist.get(city_address_code, '')
        if address_info['city'] == '':
            address_info['city'] = abandoned_address_code_dist.get(city_address_code, '')
        address_info['district'] = address_code_dist.get(address_code, '')
        if address_info['district'] == '':
            address_info['district'] = abandoned_address_code_dist.get(address_code, '')
    else:
        address_info['city'] = ''
        address_info['district'] = ''

    return address_info


def get_constellation(birthday_code):
    """
    获取星座信息
    :param birthday_code:
    :return:
    """
    year = birthday_code[0:4]
    month = birthday_code[4:6]
    day = birthday_code[6:8]
    time = func.str_to_time(birthday_code, '%Y%m%d')

    if (month == '01' and int(day) < 20) or (month == '12' and int(day) > 21):
        return data.get_constellation()['12']['name']
    elif month == '01':
        return data.get_constellation()['01']['name']
    elif month == '12':
        return data.get_constellation()['12']['name']

    start_date = func.str_to_time(year + '-' + data.get_constellation()[month]['start_date'])
    end_date = func.str_to_time(year + '-' + data.get_constellation()[month]['end_date'])
    if (start_date <= time) and (end_date >= time):
        return data.get_constellation()[month]['name']

    key = int(month) - 1
    key = func.get_str_pad(key) if key < 10 else str(key)
    start_date = func.str_to_time(year + '-' + data.get_constellation()[key]['start_date'])
    end_date = func.str_to_time(year + '-' + data.get_constellation()[key]['end_date'])
    if (start_date <= time) and (end_date >= time):
        return data.get_constellation()[key]['name']

    return ''


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



