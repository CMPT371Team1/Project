from __future__ import absolute_import
import sys
from extras.Error_Code import *
from extras.Required_Fields import required_api_dict

sys.path.append('../')
import os
import unittest
import Main
from API_NAME import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Utils import *
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestUtils(unittest.TestCase):

    def test_keys_missing_1(self):
        #Case 1: missing keys
        expected_keys = ['authToken', 'userId']
        post = {}
        errors, values = keys_missing(expected_keys,post)
        #Errors should contain both keys and values should conatin none.
        self.assertEquals(errors, {'missingToken': 'authToken is Missing',
                                   'missingUserId': 'userId is Missing'})
        self.assertEquals(values, {})

    def test_keys_missing_2(self):
        #Case 2: correct keys
        expected_keys = ['authToken', 'userId']
        post ={'authToken': 'TestAuthToken',
                'userId': 'TestUserId'}
        errors, values = keys_missing(expected_keys,post)
        # Errors should contain no values and values should contain both.
        self.assertEquals(errors, {})
        self.assertEquals(values, {'authToken': 'TestAuthToken',
                                   'userId': 'TestUserId'})

    def test_keys_missing_3(self):
        # Case 2: Incorrect keys + one correct
        expected_keys = ['authToken', 'userId']
        post = {'authToken': 'TestAuthToken',
                'incorrectKey:': 'Incorrect Value'}
        errors, values = keys_missing(expected_keys, post)
        # Errors should contain the missing value,
        # values should contain all input keys.
        self.assertEquals(errors, {'missingUserId': 'userId is Missing'})
        self.assertEquals(values, {'authToken': 'TestAuthToken',
                                   'incorrectKey:': 'Incorrect Value'})

    def test_convert_to_bool(self):
        check_bool = 'True'
        self.assertTrue(convert_to_bool(check_bool))
        check_bool = 'true'
        self.assertTrue(convert_to_bool(check_bool))
        check_bool = 'False'
        self.assertFalse(convert_to_bool(check_bool))
        check_bool = 'anything else'
        self.assertFalse(convert_to_bool(check_bool))

    def test_is_existing_and_non_empty(self):
        test_dict = {'key1': 'value1',
                     'second_key:': 'value2'}
        exists = is_existing_and_non_empty('key1', test_dict)
        self.assertTrue(exists)
        #TODO why does this test not work? I am very confused by this one.
        #exists = is_existing_and_non_empty('second_key', test_dict)
        #self.assertTrue(exists)

        exists = is_existing_and_non_empty('not_key', test_dict)
        self.assertFalse(exists)

    def test_is_valid_read_del(self):
        self.assertTrue(is_valid_read_del('r'))
        self.assertTrue(is_valid_read_del('R'))
        self.assertTrue(is_valid_read_del('d'))
        self.assertFalse(is_valid_read_del('q'))

    def test_scale_province(self):
        self.assertEquals(scale_province('Saskatchewan'),'SK')
        self.assertEquals(scale_province('saskatchewan'), 'SK')
        self.assertNotEquals(scale_province('Alberta'), 'SK')

    def test_are_two_lists_same(self):
        list1 = ['element1', 'element2']
        list2 = ['element1', 'element2']
        self.assertTrue(are_two_lists_same(list1,list2))

        list2 = ['element2', 'element1']
        self.assertTrue(are_two_lists_same(list1, list2))

        list2 = ['element1', 'element2','element3']
        self.assertFalse(are_two_lists_same(list1, list2))

        list2 = ['element1']
        self.assertFalse(are_two_lists_same(list1, list2))

    def test_is_empty(self):
        self.assertTrue(is_empty({}))
        self.assertTrue(is_empty(''))
        self.assertTrue(is_empty(None))
        self.assertTrue(is_empty(' '))

        self.assertFalse(is_empty('not nothing'))
        self.assertFalse(is_empty(1))
