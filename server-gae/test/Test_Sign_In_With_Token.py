from __future__ import absolute_import
import json
import os
import sys
sys.path.append('../')
import unittest
from extras.Error_Code import *
import Main
import webapp2
from models.User import *
from extras.Utils import *
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestSignInWithToken(unittest.TestCase):
    """
    Test case 1: Testing with missing input
    Test case 2: Testing with incorrect token
    Test case 3: Testing with incorrect user id
    Test case 4: Testing with correct information

    """

    def setUp(self):
        setup_testbed(self)
        self.database_entry = self.database_user = create_random_user()

        request = webapp2.Request.blank('/createUser', POST=self.database_entry)
        response = request.get_response(Main.app)
        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, success)
        self.user_id = json.loads(response.body)['userId']
        self.token = json.loads(response.body)['authToken']

    def test_sign_in_missing_params(self):
        # No input parameters
        input1 = {}  # Json object to send
        output, response_status = get_sign_in_token_response(input1)
        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_token['error']]
        # checking if there is a difference between error_keys and what we got
        self.assertTrue(
            are_two_lists_same(errors_expected, output.keys()))

    def test_sign_in_incorrect_token(self):
        # Test2: When incorrect token
        input2 = {'userId': self.user_id,
                  'authToken': 'ThisTokenIsNoGood'}
        output, response_status = get_sign_in_token_response(input2)

        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(
            are_two_lists_same([not_authorized['error']], output.keys()))

    def test_sign_in_incorrect_user_id(self):
        # Test2: When incorrect user_id
        input2 = {'userId': '12341',
                  'authToken': self.token}
        output, response_status = get_sign_in_token_response(input2)

        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(
            are_two_lists_same([not_authorized['error']], output.keys()))

    def test_sign_in_success(self):
        # Correct user_id and authToken
        input3 = {'userId': self.user_id,
                  'authToken': self.token}

        output, response_status = get_sign_in_token_response(input3)
        self.assertEquals(response_status, success)
        # Check output
        self.assertNotEqual(output['authToken'], self.token)
        check_output_for_sign_in(self,output,self.database_user)

        #check to make sure the old token doesn't work
        output, response_status = get_sign_in_token_response(input3)
        self.assertEquals(response_status,unauthorized_access)


    def tearDown(self):
        self.testbed.deactivate()


def get_sign_in_token_response(post):
    return get_response_from_post(Main, post, sign_in_token_api)
