from __future__ import absolute_import

import json
import os
import sys

sys.path.append('../')
import unittest
import Main
from extras.Utils import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from API_NAME import *
from extras.Utils import get_response_from_post
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestSignIn(unittest.TestCase):
    """
    Test case 1: With correct email and password.
    Test case 2: With case insensitive email
    Test case 3: with empty input
    Test case 4: incorrect password
    Test case 5: incorrect email
    """
    def setUp(self):
        setup_testbed(self)
        self.database_user = create_random_user()
        # explicitly set the email to this so that we can test case sensitivity
        self.database_user['email'] = 'student@usask.ca'
        request = webapp2.Request.blank('/createUser', POST=self.database_user)
        response = request.get_response(Main.app)
        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, success)

    def test_sign_in(self):

        # Test with correct e-mail and password
        input3 = {'email': 'student@usask.ca',
                  'password': self.database_user['password']}

        output, response_status = get_sign_in_response(input3)

        self.assertEquals(response_status, success)

        #Check output
        check_output_for_sign_in(self, output, self.database_user)

    def test_sign_in_uppercase_email(self):
        # Test with correct e-mail and password, but email is capitalized.
        input3 = {'email': 'STUDENT@usask.ca',
                  'password': self.database_user['password']}

        response, response_status = get_sign_in_response(input3)
        self.assertEquals(response_status, success)
        check_output_for_sign_in(self, response, self.database_user)

    def test_no_params(self):
        # Test1: when no paramaters are given
        input1 = {}  # Json object to send
        response, response_status = get_sign_in_response(input1)
        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [missing_password['error'],
                           missing_email['error']]

        # checking if there is a difference between error_keys and what we got
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))

    def test_incorrect_password(self):
        # Test2: When incorrect password is entered
        input2 = {'email': 'student@usask.ca',
                  'password': self.database_user['password'] + 'wrongPassword'}
        response, response_status = get_sign_in_response(input2)
        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(
            are_two_lists_same(response.keys(), [not_authorized['error']]))

    def test_incorrect_userName(self):
        # Test2: When incorrect user_name, but correct password
        input2 = {'email': 'WrongEmail@g.com',
                  'password': 'aaAA1234'}
        response, response_status = get_sign_in_response(input2)
        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(
            are_two_lists_same(response.keys(), [not_authorized['error']]))

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_sign_in_response(post):
    return get_response_from_post(Main, post, sign_in_api)
