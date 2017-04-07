from __future__ import absolute_import

import os
import sys
from extras.Check_Invalid import *
sys.path.append("../")
import unittest
from API_NAME import contact_seller_api

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *
from extras.Random_Models import *


class TestContactSeller(unittest.TestCase):
    """
    Test 1: Correct input.
    Test 2: Sending message to itself
    Test 3: Testing unauthorized user
    Test 4: Testing unauthorized listing
    Test 5: Testing with missing input
    """
    def setUp(self):
        setup_testbed(self)
        self.user_buyer = create_dummy_users_for_testing(Main, 1)[0]
        listings, user_sellers = create_dummy_listings_for_testing(Main, 1)
        self.user_seller = user_sellers[0]
        self.listing = listings[0]

    def test_correct_input(self):
        correct_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email'],
            "receiverId": self.user_seller['userId']
        }

        response, response_status = \
            get_contact_seller_api_response(correct_input)
        self.assertEquals(response_status, success)

    def test_un_allowed_input(self):
        un_allowed_input = {
            "senderId": self.user_seller['userId'],
            "listingId": self.listing['listingId'],
            "receiverId": self.user_seller['userId'],
            "authToken": self.user_seller['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = \
            get_contact_seller_api_response(un_allowed_input)

        self.assertEquals(response_status, processing_failed)
        errors_expected = [unallowed_message_send['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_unauthorized_user_id_input(self):
        unauthorized_input = {
            "senderId": 111,
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['authToken'],
            "receiverId": self.user_seller['userId'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = \
            get_contact_seller_api_response(unauthorized_input)

        self.assertEquals(response_status, not_authorized['status'])
        errors_expected = [not_authorized['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_unauthorized_listingId_input(self):
        unauthorized_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": 111,
            "receiverId": self.user_seller['userId'],
            "authToken": self.user_buyer['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = \
            get_contact_seller_api_response(unauthorized_input)

        self.assertEquals(response_status, un_auth_listing['status'])
        errors_expected = [un_auth_listing['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_missing_input(self):
        missing_input = {}
        response, response_status = \
            get_contact_seller_api_response(missing_input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_senderId['error'],
                           missing_listing_id['error'],
                           missing_message['error'],
                           missing_phone_number['error'],
                           missing_email['error'],
                           missing_token['error'],
                           missing_receiverId['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_invalid_sender(self):
        correct_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['authToken'] + "a",
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email'],
            "receiverId": self.user_seller['userId']
        }

        response, response_status = \
            get_contact_seller_api_response(correct_input)
        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(are_two_lists_same(response.keys(),
                                           [not_authorized["error"]]))



    def tearDown(self):
        self.testbed.deactivate()


def get_contact_seller_api_response(input_dictionary):
    return get_response_from_post(Main, input_dictionary, contact_seller_api)
