from __future__ import absolute_import

import sys
import unittest

import Main
from web_apis.Like_Dislike_Listing import *
from API_NAME import *
from extras.Utils import get_response_from_post
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Check_Invalid import *
from extras.Random_Models import *

class TestLikeListingApi(unittest.TestCase):
    """
        test case 1: the owner can't like their listings
        now user want to like the listing
        test case 2: successful delivery (like the listing)
        test case 3: send a like request(liked==True) while the listing is already liked
        test case 4: dislike this listing
        should be a successful delivery
        test case 5: dislike this listing again
        test case 6: missing user input
        test case 7: invalid user input
    """
    def setUp(self):
        setup_testbed(self)

        # create a user as well as a listing that the user owns
        # listings, users = create_dummy_listings_for_testing(Ma
        owner = create_dummy_users_for_testing(Main, 1)
        self.assertEquals(len(owner), 1)
        self.owner_id = owner[0]['userId']
        self.owner_token = owner[0]['authToken']
        listing = create_random_listing(self.owner_id, self.owner_token)
        listing['isPublished'] = 'True'
        response, status = get_response_from_post(Main, listing, create_listing_api)
        self.listing_id = response['listingId']

        # now create a new user as a liker
        users = create_dummy_users_for_testing(Main, 1)
        self.assertEquals(len(users), 1)
        liker = users[0]
        self.liker_id = liker['userId']
        self.liker_token = liker['authToken']

    def test_owner_liking_listing(self):
        like_the_listing = {
            "userId": self.owner_id,
            "listingId": self.listing_id,
            'authToken': self.owner_token,
            "liked": "True"
        }

        response, response_status = get_like_listing_response(like_the_listing)
        self.assertEquals(response_status, processing_failed)
        errors_expected = [unallowed_liked['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_like_listing(self):
        like_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "True"
        }

        _, response_status = get_like_listing_response(like_the_listing)
        self.assertEquals(response_status, success)

    def test_already_liked_listing(self):

        like_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "True"
        }
        _, response_status = get_like_listing_response(like_the_listing)
        self.assertEquals(response_status, success)

        response, response_status = get_like_listing_response(like_the_listing)
        self.assertEquals(response_status, processing_failed)
        errors_expected = [duplicated_liked['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_dislike_listing(self):
        dislike_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "False"
        }

        response, response_status = \
            get_like_listing_response(dislike_the_listing)
        self.assertEquals(response_status, success)

    def test_already_disliked_listing(self):

        dislike_the_listing_again = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "False"
        }

        response, response_status = \
            get_like_listing_response(dislike_the_listing_again)
        self.assertEquals(response_status, success)

        response, response_status = \
            get_like_listing_response(dislike_the_listing_again)
        self.assertEquals(response_status, processing_failed)
        errors_expected = [duplicated_liked['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_missing_user_input(self):
        like_with_missing_input = {
            "userId": "",
            "listingId": "",
            "authToken": "",
            "liked": ""
        }

        response, response_status = \
            get_like_listing_response(like_with_missing_input)

        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_listing_id['error'],
                           missing_liked['error'],
                           missing_token['error']]

        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_invalid_user_input(self):
        like_with_invalid_input = {
            "userId": "supposed to be an integer",
            "listingId": "supposed to be an integer",
            "authToken": self.liker_token,
            "liked": "supposed to be a boolean"
        }

        response, response_status = \
            get_like_listing_response(like_with_invalid_input)
        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [invalid_user_id['error'],
                           invalid_listing_id['error'],
                           invalid_liked['error']]
        self.assertTrue(are_two_lists_same(response.keys(), errors_expected))

    def test_invalid_listing_id(self):
        like_the_listing = {
            "userId": self.liker_id,
            "listingId": 100,
            "authToken": self.liker_token,
            "liked": "True"
        }
        response, response_status = get_like_listing_response(like_the_listing)
        self.assertEquals(response_status, unauthorized_access)
        self.assertTrue(are_two_lists_same(response.keys(),
                                           [un_auth_listing["error"]]))



    def tearDown(self):
        self.testbed.deactivate()


def get_like_listing_response(post):
    return get_response_from_post(Main, post, like_listing_api)


def get_favorites_response(post):
    return get_response_from_post(Main, post, get_favourites_listing_api)
