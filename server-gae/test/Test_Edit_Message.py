from __future__ import absolute_import

import os
import sys

sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *
import extras.Utils as utils
from models.Message import Message
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestEditMessage(unittest.TestCase):
    """
    Test case 1: Correct delete input
    Test case 2: Correct read input
    Test case 3: missing userId, token, messageId
    Test case 4: invalid userId, token, messageId
    Test case 5: messageId is integer but user still doesn't exist
    Test case 6: already liked listing

    """
    def setUp(self):
        setup_testbed(self)
        self.user_buyer = create_dummy_users_for_testing(Main, 1)[0]
        listings, user_sellers = create_dummy_listings_for_testing(Main,1)
        self.user_seller = user_sellers[0]
        self.listing = listings[0]
        message_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": self.listing['listingId'],
            "receiverId": self.listing['userId'],
            "authToken": self.user_buyer['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }
        get_contact_seller_api_response(message_input)

        get_message_input = {
            "userId": self.listing['userId'],
            "authToken": self.user_seller['authToken']
        }

        messages, _ = get_message_api_response(get_message_input)
        assert "messages" in messages
        assert len(messages["messages"]) == 1
        assert "messageId" in messages["messages"][0]

        self.valid_message_id_1 = int(messages["messages"][0]["messageId"])
        self.invalid_message_id_2 = 2

    def test_correct_input_read(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["authToken"],
                                          self.valid_message_id_1, 'r')
        values, response_status = get_edit_message_api_response(testing_input)
        self.assertEquals(response_status, success)
        message = Message.get_by_id(self.valid_message_id_1)
        self.assertTrue(message.received)

    def test_correct_input_delete(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["authToken"],
                                          self.valid_message_id_1, 'd')
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        self.assertEquals(response_status, success)
        message = Message.get_by_id(self.valid_message_id_1)
        self.assertIsNone(message)

    def test_missing_fields(self):
        testing_input = {}
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        error_keys = ['messageId', 'userId', 'authToken', 'readDel']
        expected_errors = [missing[key]["error"] for key in error_keys]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_invalid_field(self):
        testing_input = get_testing_input("as", "asdfjhasdkfh", "asd", "112")
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')

        error_keys = ['messageId', 'userId', 'readDel']
        expected_errors = [invalids[key]["error"] for key in error_keys]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_incorrect_message_id(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["authToken"],
                                          self.invalid_message_id_2, 'd')
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        expected_errors = [invalid_message_id["error"]]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_unauthorized_editor(self):
        self.user_seller = create_dummy_users_for_testing(Main, 1)[0]
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["authToken"],
                                          self.valid_message_id_1, 'r')
        values, response_status = get_edit_message_api_response(testing_input)
        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(values.keys(), [not_authorized["error"]])


    def test_liked_listing(self):
        self.test_correct_input_read()
        self.test_correct_input_read()


    def tearDown(self):
        self.testbed.deactivate()



def get_testing_input(user_id, user_auth_token,message_id, read_del):
    return {
        "userId": user_id,
        "authToken": user_auth_token,
        "messageId": message_id,
        "readDel": read_del
    }


def get_contact_seller_api_response(input_dictionary):
    return \
        utils.get_response_from_post(Main, input_dictionary, contact_seller_api)


def get_message_api_response(input_dictionary):
    return \
        utils.get_response_from_post(Main, input_dictionary, get_messages_api)


def get_edit_message_api_response(input_dictionary):
    return \
        utils.get_response_from_post(Main, input_dictionary, edit_message_api)
