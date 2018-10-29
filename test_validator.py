#! /usr/env/bin python
# -*- coding: utf8 -*-


import unittest
from id_validator import validator


class ValidatorTest(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(validator.is_valid('440308199901101512'))
        self.assertTrue(validator.is_valid('610104620927690'))
        self.assertTrue(validator.is_valid('810000199408230021'))
        self.assertTrue(validator.is_valid('830000199201300022'))
        self.assertTrue(validator.is_valid('500154199301135886'))

        self.assertFalse(validator.is_valid('440308199901101513'))  # 验证码不合法
        self.assertFalse(validator.is_valid('44030819990110'))  # 号码位数不合法
        self.assertFalse(validator.is_valid('111111199901101512'))  # 地址码不合法
        self.assertFalse(validator.is_valid('440308199902301512'))  # 出生日期码不合法
        self.assertFalse(validator.is_valid('610104620932690'))  # 出生日期码不合法

    def test_get_info(self):
        self.assertEqual(validator.get_info('440308199901101512'), {
            'address_code': '440308',
            'abandoned': 0,
            'address': '广东省深圳市盐田区',
            'address_tree': ['广东省', '深圳市', '盐田区'],
            'birthday_code': '1999-01-10',
            'constellation': '摩羯座',
            'chinese_zodiac': '卯兔',
            'sex': 1,
            'length': 18,
            'check_bit': '2'
        })

        self.assertEqual(validator.get_info('362324198001010014'), {
            'address_code': '362324',
            'abandoned': 1,
            'address': '江西省宜春地区丰城县',
            'address_tree': ['江西省', '宜春地区', '丰城县'],
            'birthday_code': '1980-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '申猴',
            'sex': 1,
            'length': 18,
            'check_bit': '4'
        })

        self.assertEqual(validator.get_info('362324198101010011'), {
            'address_code': '362324',
            'abandoned': 1,
            'address': '江西省宜春地区丰城县',
            'address_tree': ['江西省', '宜春地区', '丰城县'],
            'birthday_code': '1981-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '酉鸡',
            'sex': 1,
            'length': 18,
            'check_bit': '1'
        })

        self.assertEqual(validator.get_info('362324198201010019'), {
            'address_code': '362324',
            'abandoned': 1,
            'address': '江西省上饶地区铅山县',
            'address_tree': ['江西省', '上饶地区', '铅山县'],
            'birthday_code': '1982-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '戌狗',
            'sex': 1,
            'length': 18,
            'check_bit': '9',
        })

    def test_fake_id(self):
        self.assertTrue(validator.is_valid(validator.fake_id()))
        self.assertTrue(validator.is_valid(validator.fake_id(False)))
        self.assertTrue(validator.is_valid(validator.fake_id(True, '上海市', '2000', 1)))
        self.assertTrue(validator.is_valid(validator.fake_id(True, '江苏省', '20000101', 1)))
        self.assertTrue(validator.is_valid(validator.fake_id(True, '台湾省', '20131010', 0)))

    def test_upgrade_id(self):
        id_card = validator.upgrade_id('610104620927690')
        self.assertTrue(validator.is_valid(id_card))


if __name__ == '__main__':
    unittest.main()
