from __future__ import absolute_import

import copy
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


class TestGetFavouriteListing(unittest.TestCase):
    """
    Test case 1: successful get info if like a listing
    Test case 2: get expected info if dislike a listing
    Test case 3: Invalid userId
    Test case 4: liked listings from multiple users
    """
    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(listings) == 10

        # now create a new user as a liker, we'll use this person to send GetFavourites request
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        liker = users[0]
        self.likerId = liker['userId']
        self.likerToken = liker['authToken']

        # make the liker likes the first five of the listings

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[0]['listingId'],
                                                                       self.likerToken,  "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[1]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[2]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[3]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[4]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        # the first five listings has been liked, so we create a list of those listings for future use
        self.likedListings = listings[0:5]

    def test_like_success(self):

        get_favs = {
            "userId": self.likerId,
            "authToken": self.likerToken
        }
        output, response_status = get_favourites_response(get_favs)
        self.assertEquals(response_status, success)
        # get the number of published listings
        is_published = 0
        for listing in self.likedListings:
            if listing['isPublished'] == 'True':
                is_published += 1
        self.assertEquals(len(output["listings"]), is_published)

    def test_dislike_success(self):
        # dislike the last listing
        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, self.likedListings[4]['listingId'],
                                                                       self.likerToken, "False"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        liked_listings = copy.copy(self.likedListings)
        del liked_listings[-1]
        assert len(liked_listings) == 4

        get_favs = {
            "userId": self.likerId,
            "authToken": self.likerToken
        }
        output, response_status = get_favourites_response(get_favs)
        self.assertEquals(response_status, success)
        # get the number of published listings
        is_published = 0
        for listing in liked_listings:
            if listing['isPublished'] == 'True':
                is_published += 1
        self.assertEquals(len(output["listings"]), is_published)

        disliked_fav_is_deleted = 1
        for output_listing in output["listings"]:
            if output_listing['listingId'] == int(self.likedListings[-1]['listingId']):
                disliked_fav_is_deleted = 0
        self.assertEquals(disliked_fav_is_deleted, 1)

    def test_invalid_userid(self):
        invalid_favs = {
            "userId": "invalidUserId",
            "authToken": self.likerToken
        }
        response, response_status = get_favourites_response(invalid_favs)
        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [Error_Code.invalid_user_id['error']]
        # checking if there is a difference between error_keys and what we got
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))

    def test_liked_listings_from_multiple_users(self):
        another_listings, another_user = create_dummy_listings_for_testing(Main, 2)
        assert len(another_user) == 1
        assert len(another_listings) == 2

        # make the liker likes the two listings
        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, another_listings[0]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, another_listings[1]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        get_favs = {
            "userId": self.likerId,
            "authToken": self.likerToken
        }
        output, response_status = get_favourites_response(get_favs)
        self.assertEquals(response_status, success)
        
        # get the number of published listings
        is_published = 0
        for listing in self.likedListings + another_listings:
            if listing['isPublished'] == 'True':
                is_published += 1
        self.assertEquals(len(output["listings"]), is_published)

    def tearDown(self):
        self.testbed.deactivate()


def get_like_post_dictionary(user_id, listing_id, authToken, liked):
    return {"userId": user_id, "listingId": listing_id,
            "authToken": authToken, "liked": liked}


def get_like_response(post):
    return get_response_from_post(Main, post, like_listing_api)


def get_favourites_response(post):
    return get_response_from_post(Main, post, get_favourites_listing_api)
