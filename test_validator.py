#! /usr/env/bin python
# -*- coding: utf8 -*-


import unittest
from id_validator import validator
from datetime import datetime


class ValidatorTest(unittest.TestCase):
    def test_is_valid(self):
        self.assertTrue(validator.is_valid('440308199901101512'))
        self.assertTrue(validator.is_valid('610104620927690'))
        self.assertTrue(validator.is_valid('810000199408230021'))
        self.assertTrue(validator.is_valid('830000199201300022'))
        self.assertFalse(validator.is_valid('500154199301135886', True))  # 出生日期在地址码发布之前，严格模式
        self.assertTrue(validator.is_valid('500154199301135886'))  # 出生日期在地址码发布之前，非严格模式
        self.assertTrue(validator.is_valid('411082198901010002'))  # 出生日期在地址码发布之前，非严格模式
        self.assertFalse(validator.is_valid('411082198901010002', True))  # 出生日期在地址码发布之前，非严格模式
        self.assertTrue(validator.is_valid('500154199804106120'))
        self.assertFalse(validator.is_valid('440308199901101513'))  # 验证码不合法
        self.assertFalse(validator.is_valid('44030819990110'))  # 号码位数不合法
        self.assertFalse(validator.is_valid('111111199901101512'))  # 地址码不合法
        self.assertFalse(validator.is_valid('440308199902301512'))  # 出生日期码不合法
        self.assertFalse(validator.is_valid('610104620932690'))  # 出生日期码不合法
        self.assertTrue(validator.is_valid('44040119580101000X'))  # 历史遗留数据：珠海市市辖区
        self.assertTrue(validator.is_valid('140120197901010008'))  # 历史遗留数据：太原市市区

    def test_get_info(self):
        self.assertEqual(validator.get_info('440308199901101512'), {
            'address_code': '440308',
            'abandoned': 0,
            'address': '广东省深圳市盐田区',
            'address_tree': ['广东省', '深圳市', '盐田区'],
            'age': datetime.now().year - int('440308199901101512'[6:10]),
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
            'age': datetime.now().year - int('362324198001010014'[6:10]),
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
            'age': datetime.now().year - int('362324198101010011'[6:10]),
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
            'age': datetime.now().year - int('362324198201010019'[6:10]),
            'birthday_code': '1982-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '戌狗',
            'sex': 1,
            'length': 18,
            'check_bit': '9',
        })

        self.assertEqual(validator.get_info('430302199312194239'), {
            'address_code': '430302',
            'abandoned': 0,
            'address': '湖南省湘潭市雨湖区',
            'address_tree': ['湖南省', '湘潭市', '雨湖区'],
            'age': datetime.now().year - int('430302199312194239'[6:10]),
            'birthday_code': '1993-12-19',
            'constellation': '射手座',
            'chinese_zodiac': '酉鸡',
            'sex': 1,
            'length': 18,
            'check_bit': '9',
        })

        self.assertEqual(validator.get_info('411082198901010002'), {
            'address_code': '411082',
            'abandoned': 0,
            'address': '河南省许昌市长葛市',
            'address_tree': ['河南省', '许昌市', '长葛市'],
            'age': datetime.now().year - int('411082198901010002'[6:10]),
            'birthday_code': '1989-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '巳蛇',
            'sex': 0,
            'length': 18,
            'check_bit': '2',
        })

        self.assertEqual(validator.get_info('44040119580101000X'), {
            'address_code': '440401',
            'abandoned': 1,
            'address': '广东省珠海市市辖区',
            'address_tree': ['广东省', '珠海市', '市辖区'],
            'age': datetime.now().year - int('44040119580101000X'[6:10]),
            'birthday_code': '1958-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '戌狗',
            'sex': 0,
            'length': 18,
            'check_bit': 'X',
        })

        self.assertEqual(validator.get_info('140120197901010008'), {
            'address_code': '140120',
            'abandoned': 1,
            'address': '山西省太原市市区',
            'address_tree': ['山西省', '太原市', '市区'],
            'age': datetime.now().year - int('140120197901010008'[6:10]),
            'birthday_code': '1979-01-01',
            'constellation': '摩羯座',
            'chinese_zodiac': '未羊',
            'sex': 0,
            'length': 18,
            'check_bit': '8',
        })



    def test_fake_id(self):
        for i in range(100):
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
