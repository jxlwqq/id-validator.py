#!/usr/bin/env python
# encoding: utf-8

from . import utils
from . import helper
from . import data


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def is_valid(id_card):
    """
    检测身份证合法性
    :param id_card:
    :return:
    """
    id_card = str(id_card)
    code = helper.get_id_argument(id_card)
    if not helper.check_address_code(code['address_code']):
        return False

    if not helper.check_birthday_code(code['birthday_code']):
        return False

    if not helper.check_order_code(code['order_code']):
        return False

    if code['type'] == 15:
        return True

    check_bit = helper.generator_check_bit(code['body'])
    if check_bit != code['check_bit']:
        return False

    return True


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def get_info(id_card):
    """
    获取身份证信息
    :param id_card:
    :return:
    """
    id_card = str(id_card)

    if not is_valid(id_card):
        return False

    code = helper.get_id_argument(id_card)
    address_info = helper.get_address_info(code['address_code'])
    info = dict()
    info['address_code'] = code['address_code']
    info['abandoned'] = 1 if data.get_abandoned_address_code().get(code['address_code'], 0) else 0
    info['address'] = address_info['province'] + address_info['city'] + address_info['district']
    info['birthday_code'] = code['birthday_code'][0:4] + '-' + code['birthday_code'][4:6] + '-' + code['birthday_code'][
                                                                                                  6:8]
    info['constellation'] = helper.get_constellation(code['birthday_code'])
    info['chinese_zodiac'] = helper.get_chinese_zodiac(code['birthday_code'])
    info['sex'] = 0 if int(code['order_code']) % 2 == 0 else 1
    info['length'] = code['type']
    info['check_bit'] = code['check_bit']

    return info


def fake_id(eighteen=True, address=None, birthday=None, sex=None):
    """
    伪造身份证
    :param eighteen:
    :param address:
    :param birthday:
    :param sex:
    :return:
    """
    address_code = helper.generator_address_code(address)
    birthday_code = helper.generator_birthday_code(birthday)
    order_code = helper.generator_order_code(sex)

    if not eighteen:
        return address_code + birthday_code[2:] + order_code

    body = address_code + birthday_code + order_code
    check_bit = helper.generator_check_bit(body)

    return body + check_bit


@utils.check_for_none
@utils.check_empty_string
@utils.check_id_card_length
def upgrade_id(id_card):
    """
    身份证号码升级（15 位升级为 18 位）
    :param id_card:
    :return:
    """
    if not is_valid(id_card):
        return False
    code = helper.get_id_argument(id_card)
    return code['address_code'] + code['birthday_code'] + code['order_code'] + helper.generator_check_bit(code['body'])