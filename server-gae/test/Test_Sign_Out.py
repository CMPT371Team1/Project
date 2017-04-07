from __future__ import absolute_import

import os
import sys

sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *
from extras.Utils import get_response_from_post
from API_NAME import sign_out_api, sign_in_token_api
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestSignOut(unittest.TestCase):
    """
    Test1: Correct input
    Test2: Incorrect input
    """
    def setUp(self):
        setup_testbed(self)
        self.users = create_dummy_users_for_testing(Main, 1)

    def test_sign_out_incorrect_input(self):
        sign_in_user_input = get_post_dictionary(self.users[0]["userId"],
                                                 "invalidToken")

        response, response_status = get_sign_out_response(sign_in_user_input)

        self.assertEqual(response_status, unauthorized_access)

    def test_sign_out_incorrect_user_id(self):
        sign_in_user_input = get_post_dictionary( 111333311,
            self.users[0]["authToken"])

        response, response_status = get_sign_out_response(sign_in_user_input)
        self.assertEqual(response_status, unauthorized_access)

    def test_sign_out_correct_input(self):
        sign_in_user_input = get_post_dictionary(self.users[0]["userId"],
                                                 self.users[0]["authToken"])

        response, response_status = get_sign_out_response(sign_in_user_input)
        self.assertEqual(response_status, success)

        _, response_status = get_sign_in_response(sign_in_user_input)

        self.assertEqual(response_status, unauthorized_access)






        pass

    def tearDown(self):
        self.testbed.deactivate()


def get_post_dictionary(userId, token):
    return {"userId": userId, "authToken": token}


def get_sign_out_response(post):
    return get_response_from_post(Main, post, sign_out_api)


def get_sign_in_response(post):
    return get_response_from_post(Main, post, sign_in_token_api)
