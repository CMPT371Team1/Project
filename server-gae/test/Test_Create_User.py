from __future__ import absolute_import
import os
import sys
sys.path.append("../")
import unittest
import Main
from models.FacebookUser import FacebookUser
from extras.Utils import *
from API_NAME import create_user_api
from extras.Check_Invalid import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Random_Models import *


class TestCreateUser(unittest.TestCase):
    """

    Test case 1: Different kinds of empty strings and null values
    Test case 2: Test with invalid phone 1
    Test case 3: Test with invalid phone 2
    Test case 4: Test with invalid email address
    Test case 5: Test with not strong password
    Test case 6: Test to check if email already exists
    Test case 7: Test all valid fields without facebook
    Test case 8: Test all valid fields with facebook
    """
    def setUp(self):
        setup_testbed(self)

    def test_missing_fields(self):
        empty_input = {
            "email": "  ",
            "lastName": ""
        }

        response_body, status_int = get_create_user_api_response(empty_input)

        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [missing_province['error'],
                           missing_confirmed_password['error'],
                           missing_password['error'],
                           missing_phone_number['error'],
                           missing_first_name['error'],
                           missing_city['error'],
                           missing_email['error']]

        error_keys = [str(x) for x in response_body]
        self.assertEquals(are_two_lists_same(error_keys,errors_expected), True)

    def test_invalid_phone1(self):
        invalid_phone1_input = create_random_user()
        invalid_phone1_input['phone1'] = "123456"
        response_body, status_int = \
            get_create_user_api_response(invalid_phone1_input)

        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_phone1['error']]
        error_keys = [str(x) for x in response_body]

        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_invalid_phone2(self):
        invalid_phone2_input = create_random_user()
        invalid_phone2_input['phone2'] = "123456"
        response_body, status_int = \
            get_create_user_api_response(invalid_phone2_input)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_phone2['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_invalid_email(self):
        invalid_email_input = create_random_user()
        invalid_email_input['email'] = "gaa"
        response_body, status_int = \
            get_create_user_api_response(invalid_email_input)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_email['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_not_strong_password(self):
        not_strong_pass_input = create_random_user()
        not_strong_pass_input['password'] = "123456"
        not_strong_pass_input['confirmedPassword'] = "123456"
        response_body, status_int = \
            get_create_user_api_response(not_strong_pass_input)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [password_not_strong['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_password_mismatch(self):
        mismatch_password_input = create_random_user()
        mismatch_password_input['confirmedPassword'] = "123456"

        response, status_int = \
            get_create_user_api_response(mismatch_password_input)

        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [password_mismatch['error']]
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))

    def test_create_user_without_fb(self):
        user_input = create_random_user()
        response_body, status_int = get_create_user_api_response(user_input)
        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))

        self.assertTrue(user_saved.compare_with_dictionary(user_input))



    def test_duplicate_email(self):
        user_input = create_random_user()
        _, status_int = get_create_user_api_response(user_input)
        self.assertEquals(status_int, success)
        response, status_int = get_create_user_api_response(user_input)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [email_alreadyExists['error']]
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))

    def test_create_user_with_fb(self):
        fb_user = create_random_user()
        fb_user["fbId"] = "1212312398"
        response_body, status_int = \
            get_create_user_api_response(fb_user)

        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)

        user_saved = User.get_by_id(int(response_body["userId"]))

        self.assertTrue(user_saved.compare_with_dictionary(fb_user))

        fb_e_id = FacebookUser.query().fetch(keys_only=True)[0].integer_id()

        fb_e = FacebookUser.get_by_id(fb_e_id)

        self.assertEquals(fb_e.user_id,int(response_body["userId"]))
        self.assertEquals(fb_e.fb_id, int(fb_user["fbId"]))

    def test_success_without_optional(self):
        user_input = create_random_user()
        if "phone2" in user_input:
            del user_input["phone2"]
        response_body, status_int = get_create_user_api_response(user_input)
        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))

        self.assertTrue(user_saved.compare_with_dictionary(user_input))

    def tearDown(self):
        self.testbed.deactivate()


def get_create_user_api_response(input_dictionary):
    """
    Method gets response from the createUser API and returns that.
    :param input_dictionary: input_dictionary is used as a request for the API
    call.
    :return: A tuple (dictionary, int) where dictionary has response body
    and int contains the status code returned.
    """
    return get_response_from_post(Main, input_dictionary, create_user_api)
