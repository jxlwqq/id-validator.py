#! /usr/env/bin python
# -*- coding: utf8 -*-


import unittest
from id_validator import validator


class ValidatorTest(unittest.TestCase):
    def test_is_valid(self):
        self.assertEquals(validator.is_valid('440308199901101512'), True)
        self.assertEquals(validator.is_valid('610104620927690'), True)
        self.assertEquals(validator.is_valid('810000199408230021'), True)
        self.assertEquals(validator.is_valid('830000199201300022'), True)
        self.assertEquals(validator.is_valid('440308199901101513'), False)

    def test_get_info(self):
        self.assertEquals(validator.get_info('440308199901101512'), {
            'address_code': '440308',
            'abandoned': 0,
            'address': '广东省深圳市盐田区',
            'birthday_code': '1999-01-10',
            'constellation': '水瓶座',
            'chinese_zodiac': '卯兔',
            'sex': 1,
            'length': 18,
            'check_bit': '2'
        })

    def test_fake_id(self):
        self.assertEquals(validator.is_valid(validator.fake_id()), True)
        self.assertEquals(validator.is_valid(validator.fake_id(False)), True)
        self.assertEquals(validator.is_valid(validator.fake_id(True, '上海市', '2000', 1)), True)
        self.assertEquals(validator.is_valid(validator.fake_id(True, '江苏省', '20000101', 1)), True)
        self.assertEquals(validator.is_valid(validator.fake_id(True, '台湾省', '20131010', 0)), True)


if __name__ == '__main__':
    unittest.main()
