from __future__ import absolute_import

import os
import sys
sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Utils import *
from models.User import User
import Main
from models.FacebookUser import FacebookUser
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *

class TestFacebookLogin(unittest.TestCase):
    """
    Test case 1: successful login
    """

    def setUp(self):
        setup_testbed(self)
        self.users = create_dummy_users_for_testing(Main, 3)
        input = create_random_user()
        input["fbId"] = "1212312398"

        response_body, status_int = get_create_user_response(input)

        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))
        self.assertEquals(user_saved.first_name,input["firstName"])
        self.assertEquals(user_saved.last_name,input["lastName"])
        self.assertEquals(user_saved.city,input["city"])
        self.assertEquals(user_saved.email,input["email"])
        self.assertEquals(user_saved.phone1,input["phone1"])
        self.assertEquals(user_saved.province,input["province"])
        fb_e_id = FacebookUser.query().fetch(keys_only=True)[0].integer_id()
        fb_e = FacebookUser.get_by_id(fb_e_id)
        self.assertEquals(fb_e.user_id,int(response_body["userId"]))
        self.assertEquals(fb_e.fb_id, int(input["fbId"]))

    def test_invalid_fb_id(self):
        response, response_status = \
            get_fb_login_response({"fbId": "invalid"})
        self.assertEqual(response_status, missing_invalid_parameter)
        self.assertTrue(are_two_lists_same(response.keys(),
                                           [invalid_fb_id["error"]]))

    def test_success_facebook_login(self):
        response, response_status = \
            get_fb_login_response({"fbId": 1212312398})
        self.assertEqual(response_status, success)

    def test_unsuccess_facebook_login(self):
        response, response_status = \
            get_fb_login_response({"fbId": 121231239})
        error_list = [invalid_fb_id["error"]]
        self.assertTrue(are_two_lists_same(error_list, response.keys()))



def get_create_user_response(input_dictionary):
    return \
        get_response_from_post(Main, input_dictionary, create_user_api)


def get_fb_login_response(input_dictionary):
    return \
        get_response_from_post(Main, input_dictionary, fb_login_api)
