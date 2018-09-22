#!/usr/bin/env python
# encoding: utf-8

from . import utils
from . import data
import re
import random
import datetime


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def is_valid(id_card):
    id_card = str(id_card)
    code = __get_id_argument(id_card)
    if not __check_address_code(code['address_code']):
        return False

    if not __check_birthday_code(code['birthday_code']):
        return False

    if not __check_order_code(code['order_code']):
        return False

    if code['type'] == 15:
        return True

    check_bit = __generator_check_bit(code['body'])
    if check_bit != code['check_bit']:
        return False
    return True


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def get_info(id_card):
    id_card = str(id_card)
    if not is_valid(id_card):
        return False
    code = __get_id_argument(id_card)
    address_info = __get_address_info(code['address_code'])
    info = dict()
    info['address_code'] = code['address_code']
    info['abandoned'] = 1 if data.get_abandoned_address_code().get(code['address_code'], 0) else 0
    info['address'] = ''.join(address_info.values())
    info['birthday_code'] = code['birthday_code'][0:4] + '-' + code['birthday_code'][4:6] + '-' + code['birthday_code'][
                                                                                                  6:8]
    info['constellation'] = __get_constellation(code['birthday_code'])
    info['chinese_zodiac'] = __get_chinese_zodiac(code['birthday_code'])
    info['sex'] = 0 if int(code['order_code']) % 2 == 0 else 1
    info['length'] = code['type']
    info['check_bit'] = code['check_bit']
    return info


def fake_id(eighteen=True, address=None, birthday=None, sex=None):
    address_code = __generator_address_code(address)
    birthday_code = __generator_birthday_code(birthday)
    order_code = __generator_order_code(sex)
    if not eighteen:
        return address_code + birthday_code[2:] + order_code
    body = address_code + birthday_code + order_code
    check_bit = __generator_check_bit(body)
    return body + check_bit


def __generator_birthday_code(birthday=None):
    year = ''
    month = ''
    day = ''
    if not (birthday is None):
        year = utils.get_str_pad(birthday[0:4], 4)
        month = utils.get_str_pad(birthday[4:6], 2)
        day = utils.get_str_pad(birthday[6:8], 2)

    if year == '' or year < '1800' or year > str(datetime.datetime.now().year):
        year = '19' + str(random.randint(50, 100))

    if month == '' or month == '00' or month > '12':
        month = utils.get_str_pad(random.randint(1, 12))

    if day == '' or day == '00' or day > '31':
        day = utils.get_str_pad(random.randint(1, 28))

    if not utils.check_date(month, day, year):
        year = '19' + str(random.randint(50, 100))
        month = utils.get_str_pad(random.randint(1, 12))
        day = utils.get_str_pad(random.randint(1, 28))

    birthday_code = year + month + day
    return birthday_code


def __generator_order_code(sex=None):
    order_code = random.randint(101, 1000)
    if sex == 1:
        order_code = order_code - 1 if order_code % 2 == 0 else order_code
    if sex == 0:
        order_code = order_code if order_code % 2 == 0 else order_code - 1
    return str(order_code)


def __generator_address_code(address=None):
    address_code = ''
    if not (address is None):
        for key, val in data.get_address_code().items():
            if val == address:
                address_code = key

    if address_code != '' and address_code[0:1] == '8':
        return address_code

    if address_code != '':
        if address_code[2:6] == '0000':
            province_code = address_code[0:2]
            pattern = '^' + province_code + '\d{2}[^0]{2}$'
            pattern = re.compile(pattern)
            result = []
            for key, val in data.get_address_code().items():
                if re.match(pattern, key):
                    result.append(key)
            address_code = result[random.choice(range(len(result)))]

        if address_code[4:6] == '00':
            city_code = address_code[0:4]
            pattern = '^' + city_code + '[^0]{2}$'
            pattern = re.compile(pattern)
            result = []
            for key, val in data.get_address_code().items():
                if re.match(pattern, key):
                    result.append(key)
            address_code = result[random.choice(range(len(result)))]

    else:
        pattern = '^\d{4}[^0]{2}$'
        pattern = re.compile(pattern)
        result = []
        for key, val in data.get_address_code().items():
            if re.match(pattern, key):
                result.append(key)
        address_code = result[random.choice(range(len(result)))]

    return address_code


def __generator_check_bit(body):
    pos_weight = {}
    weight_list = range(2, 19)[::-1]
    for i in weight_list:
        weight = pow(2, i - 1) % 11;
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


def __check_address_code(address_code):
    address_info = __get_address_info(address_code)
    if address_info['province'] == '':
        return False
    return True


def __check_birthday_code(birthday_code):
    year = int(birthday_code[0:4])
    month = int(birthday_code[4:6])
    day = int(birthday_code[6:8])

    if year < 1800:
        return False

    if not utils.check_date(month, day, year):
        return False
    return True


def __check_order_code(order_code):
    if len(order_code) != 3:
        return False
    return True


def __get_id_argument(id_card):
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


def __get_address_info(address_code):
    address_info = {}
    first_character = address_code[0:1]  # 用于判断是否是港澳台居民居住证（8字开头）

    provice_address_code = address_code[0:2] + '0000'
    city_address_code = address_code[0:4] + '00'

    address_code_dist = data.get_address_code()
    abandoned_address_code_dist = data.get_abandoned_address_code()
    address_info['province'] = address_code_dist.get(provice_address_code, '')

    if address_info['province'] == '':
        address_info['province'] = abandoned_address_code_dist.get(provice_address_code, '')

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


def __get_constellation(birthday_code):
    year = birthday_code[0:4]
    month = birthday_code[4:6]
    day = birthday_code[6:8]
    time = utils.str_to_time(birthday_code)

    if (month == '01' and int(day) < 20) or (month == '12' and int(day) > 21):
        return data.get_constellation()['12']['name']
    elif month == '01':
        return data.get_constellation()['01']['name']
    elif month == '12':
        return data.get_constellation()['12']['name']

    start_date = year + '-' + data.get_constellation()[month]['start_date']

    end_date = year + '-' + data.get_constellation()[month]['end_date']

    if (utils.str_to_time(start_date, '%Y-%m-%d') <= time) and (utils.str_to_time(end_date, '%Y-%m-%d') >= time):
        return data.get_constellation()[month]['name']

    key = int(month) - 1
    key = utils.get_str_pad(key) if len(key) == 1 else str(key)
    start_date = year + '-' + data.get_constellation()[key]['start_date']
    end_date = year + '-' + data.get_constellation()[key]['end_date']
    if (utils.str_to_time(start_date, '%Y-%m-%d') <= time) and (utils.str_to_time(end_date, '%Y-%m-%d') >= time):
        return data.get_constellation()[key]['name']
    return ''


def __get_chinese_zodiac(birthday_code):
    start = 1900
    end = int(birthday_code[0:4])
    key = (end - start) % 12
    key = key if key >= 0 else key + 12
    return data.get_chinese_zodiac()[key]
