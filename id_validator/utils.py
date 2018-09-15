#!/usr/bin/env python
# encoding: utf-8

import functools


def check_for_none(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] is None:
            return False
        return func(*args, **kwargs)

    return decorator


def check_empty_string(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) == 0:
            return False
        return func(*args, **kwargs)

    return decorator


def check_id_card_length(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) != 15 and len(args[0]) != 18:
            return False
        return func(*args, **kwargs)

    return decorator


def check_date(m, d, y):
    import datetime
    try:
        m, d, y = map(int, (m, d, y))
        datetime.date(y, m, d)
        return True
    except ValueError:
        return False


def get_str_pad(string, length=2, character='0', right=False):
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


def str_to_time(string, format_string="%Y%m%d"):
    import time
    str_time = time.strptime(string, format_string)
    return int(time.mktime(str_time))
