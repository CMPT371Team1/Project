from __future__ import absolute_import
import sys

sys.path.append('../')
import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Check_Invalid import *


class TestInvalidCheck(unittest.TestCase):
    def test_is_valid_integer(self):
        """
        Testing case 1: String with more than a digit
        Testing case 2: String with only one digit
        Testing case 3: more than a digit number
        Testing case 4: 1 digit number
        Testing case 5: 0
        Testing case 6: With an alphabet
        Testing case 7: Floating point number
        Testing case 8: Floating point number
        Testing case 9: Empty
        """
        self.assertTrue(is_valid_integer("123"))
        self.assertTrue(is_valid_integer("1"))
        self.assertTrue(is_valid_integer(123))
        self.assertTrue(is_valid_integer(1))
        self.assertTrue(is_valid_integer(0))
        self.assertFalse(is_valid_integer("123A"))
        self.assertFalse(is_valid_integer("123.1"))
        self.assertFalse(is_valid_integer("123.0"))
        self.assertFalse(is_valid_integer(""))

    def test_is_valid_float(self):
        """
        Testing case 1: String with more than a digit
        Testing case 2: String with only one digit
        Testing case 3: more than a digit number
        Testing case 4: 1 digit number
        Testing case 5: 0
        Testing case 6: With an alphabet
        Testing case 7: Floating point number
        Testing case 8: Floating point number
        Testing case 9: Empty
        """
        self.assertTrue(is_valid_float("123"))
        self.assertTrue(is_valid_float("1"))
        self.assertTrue(is_valid_float(123))
        self.assertTrue(is_valid_float(1))
        self.assertTrue(is_valid_float(0))
        self.assertFalse(is_valid_float("123A"))
        self.assertTrue(is_valid_float("123.1"))
        self.assertTrue(is_valid_float("123.0"))
        self.assertFalse(is_valid_float(""))

    def test_is_valid_bathroom(self):
        """
        Test case 1: testing with 0.5
        Test case 2: testing with 1
        Test case 3: testing with 0
        Test case 4: testing with 1.0
        Test case 5: testing with 1 as a string
        Test case 6: testing with 0.5 as a string
        Test case 7: testing with 2.5
        Test case 8: testing with 2.3 not an integral multiple of 0.5
        Test case 9: testing with 2.90 not an integral multiple of 0.5
        Test case 10: testing with 2.45 not an integral multiple of 0.5
        """
        self.assertTrue(is_valid_bathroom(0.5))
        self.assertTrue(is_valid_bathroom(1))
        self.assertTrue(is_valid_bathroom(0))
        self.assertTrue(is_valid_bathroom(1.0))
        self.assertTrue(is_valid_bathroom("1"))
        self.assertTrue(is_valid_bathroom("0.5"))
        self.assertTrue(is_valid_bathroom(2.5))
        self.assertFalse(is_valid_bathroom(2.3))
        self.assertFalse(is_valid_bathroom(2.90))
        self.assertFalse(is_valid_bathroom(2.45))
        self.assertFalse(is_valid_bathroom(-1.0))

    def test_is_valid_bool(self):
        """
        Test case 1: Testing with Boolean operator: True
        Test case 2: Testing with Boolean operator: False
        Test case 3: Testing with number 1
        Test case 4: Testing with String True
        Test case 5: Testing with String False
        Test case 6: Testing with String 0
        Test case 7: Testing with empty string
        Test case 8: Testing with some number
        Test case 9: Testing with some word
        Test case 10: Testing with some Alphanumberic
        :return:
        """
        self.assertTrue(is_valid_bool(True))
        self.assertTrue(is_valid_bool(False))
        self.assertTrue(is_valid_bool(1))
        self.assertTrue(is_valid_bool("True"))
        self.assertTrue(is_valid_bool("False"))
        self.assertTrue(is_valid_bool("0"))
        self.assertFalse(is_valid_bool(""))
        self.assertFalse(is_valid_bool("123"))
        self.assertFalse(is_valid_bool("ABC"))
        self.assertFalse(is_valid_bool("A1"))

    def test_is_valid_json(self):
        """
        Test case 1: With not string
        Test case 2: With empty string
        Test case 3: With invalid string
        Test case 4: With valid string
        :return:
        """

        self.assertFalse(is_valid_json(121))
        self.assertFalse(is_valid_json(""))
        self.assertFalse(is_valid_json("ABC"))
        self.assertTrue(
            is_valid_json('{"value": "New", "onclick": "CreateNewDoc()"}'))

    def test_is_valid_phone(self):
        """
        Test case 1: valid number
        Test case 2: invalid number
        Test case 3: invalid number
        :return:
        """
        self.assertTrue(is_valid_phone(1234123412))
        self.assertTrue(is_valid_phone("1234123412"))
        self.assertFalse(is_valid_phone(12341234121))
        self.assertFalse(is_valid_phone(0))
        self.assertFalse(is_valid_phone("TENDIGITLO"))

    def test_is_valid_password(self):
        """
        Test case 1: Total numeric
        Test case 1: Total numeric as a string
        Test case 1: Total upper Alphabetic as a string
        Test case 1: Total lower Alphabetic as a string
        Test case 1: Total Alphabetic as a string
        Test case 1: Total Alphabetic and numeric as a string
        :return:
        """
        self.assertFalse(is_valid_password(1234123412))
        self.assertFalse(is_valid_password("1234123412"))
        self.assertFalse(is_valid_password("ABCDEFGHIJK"))
        self.assertFalse(is_valid_password("abcdefghijk"))
        self.assertFalse(is_valid_password("abcdeABCDE"))
        self.assertTrue(is_valid_password("abcdeABCDE1"))

    def test_is_valid_province(self):
        """
        Test case 1: Valid province ("sk")
        Test case 2: Valid province ("SK")
        Test case 3: Valid province ("Saskatchewan")
        Test case 4: Invalid province ("Saskatchewn")
        Test case 5: Invalid province ("12")
        :return:
        """
        self.assertTrue(is_valid_province("sk"))
        self.assertTrue(is_valid_province("SK"))
        self.assertTrue(is_valid_province("Saskatchewan"))
        self.assertFalse(is_valid_province("Saskatchewn"))
        self.assertFalse(is_valid_province("12"))
        self.assertFalse(is_valid_province("1"))

    def test_is_valid_email(self):
        """
        Test case 1: Valid email
        Test case 2: Valid email
        Test case 3: Valid email
        Test case 4: inValid email
        :return:
        """
        self.assertTrue(is_valid_email("abc123@mail.usask.ca"))
        self.assertTrue(is_valid_email("abc123@mail.usask"))
        self.assertTrue(is_valid_email("abc123@mail.usask"))
        self.assertFalse(is_valid_email("abc123"))

    def test_is_valid_postal_code(self):
        """
        Test case 1: Valid province with space
        Test case 2: Valid province without space
        Test case 3: Invalid province
        Test case 4: Invalid province
        :return:
        """
        self.assertTrue(is_valid_postal_code("S7N 1J7"))
        self.assertTrue(is_valid_postal_code("S7N1J7"))
        self.assertFalse(is_valid_postal_code("S7N1JP"))
        self.assertFalse(is_valid_postal_code("27N1JP"))
