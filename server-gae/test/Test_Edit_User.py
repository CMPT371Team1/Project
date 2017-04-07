from __future__ import absolute_import

import os
import sys
sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Utils import *
from models.User import User
import Main
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *

class TestEditUser(unittest.TestCase):
    """
    Test case 1: nothing requested to change
    Test case 2: email already exists
    Test case 3: unrecognized key
    Test case 4: invalid userId
    Test case 5: missing userId
    Test case 6: password can't be changed
    Test case 7: 1 item changed
    Test case 8: 2 items changed
    Test case 9: many items changed
    """

    def setUp(self):
        setup_testbed(self)
        self.users = create_dummy_users_for_testing(Main, 3)

    def test_nothing_requsted_to_change(self):
        user_id = self.users[0]["userId"]
        token = self.users[0]["authToken"]
        change_values = {}

        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))

        self.assertEqual(status, nothing_requested_to_change["status"])
        self.assertTrue(nothing_requested_to_change["error"] in res_value)

    def test_unrecognized_key(self):
        user_id = self.users[0]["userId"]
        token = self.users[0]["authToken"]
        change_values = {"unRecongnized" :"key"}

        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))

        self.assertEqual(status, unrecognized_key["status"])
        self.assertTrue(unrecognized_key["error"] in res_value)

    def test_invalid_user_id(self):
        token = self.users[0]["authToken"]
        change_values = {"phone1" :"1234567891"}
        user_id = 1000

        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, not_authorized["status"])
        self.assertTrue(not_authorized["error"] in res_value)

    def test_missing_user_id(self):
        change_values = {"phone1" :"1234567891"}
        token = self.users[0]["authToken"]
        user_id = ""
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, missing_user_id["status"])
        self.assertTrue(missing_user_id["error"] in res_value)

    def test_password_change(self):
        user_id = self.users[0]["userId"]
        token = self.users[0]["authToken"]
        change_values = {"password" :"1234567891"}
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, password_cant_be_changed["status"])
        self.assertTrue(password_cant_be_changed["error"] in res_value)

    def test_change_one_item(self):
        user_id = self.users[0]["userId"]
        token = self.users[0]["authToken"]
        change_values = {"phone1": "1234567891"}

        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))

        self.assertEqual(status, success)

        new_user = User.get_by_id(int(self.users[0]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])

    def test_two_item_change(self):
        user_id = self.users[1]["userId"]
        token = self.users[1]["authToken"]
        change_values = {"phone1": "1234567891", "firstName": "Hello"}
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, success)

        new_user = User.get_by_id(int(self.users[1]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])
        self.assertEqual(new_user.first_name, change_values["firstName"])

    def test_multi_item_change(self):
        user_id = self.users[2]["userId"]
        token = self.users[2]["authToken"]
        change_values = {"phone1": "1234567891", "firstName": "hello",
                         "lastName": "world"}
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))

        self.assertEqual(status, success)
        new_user = User.get_by_id(int(self.users[2]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])
        self.assertEqual(new_user.last_name, change_values["lastName"])

    def test_invalid_key(self):
        user_id = self.users[1]["userId"]
        token = self.users[1]["authToken"]
        change_values = {"phone1": "123", "firstName": "Hello"}
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, missing_invalid_parameter)
        self.assertTrue(res_value.keys(), [invalid_phone1["status"]])

    def test_change_email(self):
        user_id = self.users[1]["userId"]
        token = self.users[1]["authToken"]
        change_values = {"email": "something@else.com"}
        res_value, status = get_edit_message_response(
            get_post_dictionary(user_id, token, change_values))
        self.assertEqual(status, success)
        res_value, status = get_response_from_post(
            Main,
            {
                "email": change_values["email"],
                "password": self.users[1]["password"]
            },
            sign_in_api
        )

        self.assertEqual(status, success)

        res_value, status = get_response_from_post(
            Main,
            {
                "email": self.users[1]["email"],
                "password": self.users[1]["password"]
            },
            sign_in_api
        )

        self.assertEqual(status, unauthorized_access)


    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_post_dictionary(userId, token, change_values):
    return {"userId": userId, "authToken":
        token,"changeValues": json.dumps(change_values)}


def get_edit_message_response(input_dictionary):
    return get_response_from_post(Main, input_dictionary, edit_user_api)
