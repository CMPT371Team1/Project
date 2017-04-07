from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *
from extras.Utils import get_response_from_post
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestGetMessages(unittest.TestCase):
    """
    Test case 1: With valid input
    Test case 2: With invalid user id
    """
    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(listings) == 10
        self.seller = users[0]
        self.listings = listings

        self.messagers = create_dummy_users_for_testing(Main, 3)
        assert len(self.messagers) == 3

        res_value, status = get_contact_response(
            get_contact_seller_post_dictionary(
                self.messagers[0]['userId'],
                self.seller['userId'],
                self.listings[0]['listingId'],
                self.messagers[0]['authToken'],
                "Interested in your listing!",
                self.messagers[0]['phone1'],
                self.messagers[0]['email']))

        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_contact_response(
            get_contact_seller_post_dictionary(
                self.messagers[1]['userId'],
                self.seller['userId'],
                self.listings[1]['listingId'],
                self.messagers[1]['authToken'],
                "Any time we can meet up?",
                self.messagers[1]['phone1'],
                self.messagers[1]['email']))

        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_contact_response(
            get_contact_seller_post_dictionary(
                self.messagers[2]['userId'],
                self.seller['userId'],
                self.listings[2]['listingId'],
                self.messagers[2]['authToken'],
                "Nice house!",
                self.messagers[2]['phone1'],
                self.messagers[2]['email']))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

    def test_success(self):
        get_messages = {
            "userId": self.seller['userId'],
            "authToken": self.seller['authToken']
        }
        output, response_status = get_messages_response(get_messages)
        self.assertEquals(response_status, success)
        self.assertEquals(len(output['messages']), 3)

    def test_invalid_userid(self):
        invalid_user_id_messages = {
            "userId": "blablabla",
            "authToken": self.seller['authToken']
        }

        response, response_status = get_messages_response(
            invalid_user_id_messages)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [Error_Code.invalid_user_id['error']]

        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def tearDown(self):
        self.testbed.deactivate()


def get_contact_seller_post_dictionary(sender_id, receiver_id, listing_id,
                                       auth_token, message, phone, email):
    return {
            "senderId": sender_id,
            "receiverId": receiver_id,
            "listingId": listing_id,
            "authToken": auth_token,
            "message": message,
            "phone": phone,
            "email": email
        }


def get_contact_response(post):
    return get_response_from_post(Main, post, contact_seller_api)


def get_messages_response(post):
    return get_response_from_post(Main, post, get_messages_api)
