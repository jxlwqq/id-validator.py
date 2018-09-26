#!/usr/bin/env python
# encoding: utf-8

from . import utils
from . import helper


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
    info = helper.get_id_info(address_info, code)

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
