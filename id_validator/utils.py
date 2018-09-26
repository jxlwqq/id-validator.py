#!/usr/bin/env python
# encoding: utf-8

import functools


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
