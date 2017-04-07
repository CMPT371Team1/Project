from __future__ import absolute_import

import os
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *
from extras.Utils import get_response_from_post
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *


class TestGetListings(unittest.TestCase):
    """
        test case 1: empty input, only return listingIds
        test case 2: empty filer and valuesRequired, only return listingIds
        test case 3: unrecognized key in filter
        test case 4: unrecognized key in filter
        test case 5: unrecognized key in filter
        test case 6: get get listings with listingIdList
        test case 7: get listings with filter and userid
        test case 8: invalid key in valuesRequired
        test case 9: negative filter value input

    """

    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        self.listings, users = create_dummy_listings_for_testing(Main, 20)
        self.assertEquals(len(users), 1)
        self.assertEquals(len(self.listings), 20)
        self.ownerId = users[0]['userId']

        users = create_dummy_users_for_testing(Main, 1)
        self.assertEquals(len(users), 1)
        self.userId = users[0]['userId']
        self.token = users[0]['authToken']

        # make the user like a few listings
        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[0]['listingId'],
                                                                       self.token, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[1]['listingId'],
                                                                       self.token, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[2]['listingId'],
                                                                       self.token, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[3]['listingId'],
                                                                       self.token, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[4]['listingId'],
                                                                       self.token, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

    def test_empty_input(self):
        get_filter_listings = {}

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        for value in res_value:
            self.assertTrue("listingId" in value)

    def test_empty_filter(self):
        get_filter_listings = {
            "valuesRequired": "",
            "filter": "",
            "maxLimit": 5
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        for value in res_value:
            self.assertTrue("listingId" in value)

    def test_unrecognized_key_2(self):
        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "authToken": self.token,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000,
                    "what": "is_this"
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "province": "Saskatchewan"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = invalid_filter_bound['error']

        self.assertTrue(error_expected in res_value)

    def test_unrecognized_key_3(self):
        get_filter_listings = {
            "valuesRequired": json.dumps(
                ["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "authToken": self.token,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "province": "Saskatchewan",
                "what_the_heck": "is_this"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = unrecognized_key['error']

        self.assertTrue(error_expected in res_value)

    def test_get_listing_with_id(self):
        get_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address"]),
            "maxLimit": 8,
            "listingIdList": json.dumps([self.listings[0]['listingId'],
                                         self.listings[1]['listingId'],
                                         self.listings[2]['listingId'],
                                         self.listings[3]['listingId'],
                                         self.listings[4]['listingId'],
                                         self.listings[5]['listingId'],
                                         self.listings[6]['listingId']])
        }

        res_value, status = get_listing_response(get_listings)
        self.assertEqual(status, success)
        self.assertEquals(len(res_value), 7)

    def test_get_listing_with_filter(self):
        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "authToken": self.token,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "squareFeet":
                    {
                        "lower": 10,
                        "upper": 200
                    },
                "province": "Saskatchewan"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        for value in res_value:
            self.assertEquals(len(value), 5)
            self.assertTrue(int(value['price']) <=
                            int(json.loads(get_filter_listings['filter'])['price']['upper']))
            self.assertTrue(int(value['price']) >=
                            int(json.loads(get_filter_listings['filter'])['price']['lower']))
            self.assertTrue(int(value['bedrooms']) <=
                            int(json.loads(get_filter_listings['filter'])['bedrooms']['upper']))
            self.assertTrue(int(value['bedrooms']) >=
                            int(json.loads(get_filter_listings['filter'])['bedrooms']['lower']))
            self.assertTrue(float(value['bathrooms']) <=
                            float(json.loads(get_filter_listings['filter'])['bathrooms']['upper']))
            self.assertTrue(float(value['bathrooms']) >=
                            float(json.loads(get_filter_listings['filter'])['bathrooms']['lower']))

        #######################
        # make sure that the filter is reset to default after being customized
        get_filter_listings = {}

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        for value in res_value:
            self.assertTrue("listingId" in value)

    def test_invalid_key_values_required(self):
        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price", "what_the_heck"]),
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = invalid_values_required['error']

        self.assertTrue(error_expected in res_value)

    def test_negative_numeric_fields_in_filter(self):
        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "authToken": self.token,
            "filter": json.dumps({
                "price": {
                    "lower": -100,
                    "upper": -8000000
                },
                "bedrooms": {
                    "lower": -1,
                    "upper": -1000
                },
                "bathrooms": {
                    "lower": -1.0,
                    "upper": -200
                },
                "province": "Saskatchewan"
            })
        }
        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = invalid_filter_bound['error']

        self.assertTrue(error_expected in res_value)

    def test_with_filer_listing_id(self):
        get_filter_listings = {
            "valuesRequired": "",
            "filter": "",
            "listingIdList": [1, 2]
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        self.assertTrue(are_two_lists_same(res_value.keys(),
                                           [invalid_xor_condition["error"]]))

    def test_with_invalid_user_id(self):
        get_filter_listings = {
            "valuesRequired": "",
            "filter": "",
            "userId": 1000,
            "authToken": self.token
        }
        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, unauthorized_access)
        self.assertTrue(are_two_lists_same(res_value.keys(),
                                           [not_authorized["error"]]))

    def test_with_invalid_token(self):
        get_filter_listings = {
            "valuesRequired": "",
            "filter": "",
            "userId": self.userId,
            "authToken": "invalidToken"
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, unauthorized_access)
        self.assertTrue(are_two_lists_same(res_value.keys(),
                                           [not_authorized["error"]]))

    def test_with_missing_token(self):
        get_filter_listings = {
            "valuesRequired": "",
            "filter": "",
            "userId": self.userId
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, unauthorized_access)
        self.assertTrue(are_two_lists_same(res_value.keys(),
                                           [missing_token["error"]]))




def get_like_post_dictionary(user_id, listing_id, token, liked):
    return {"userId": user_id, "listingId":
            listing_id, "authToken": token, "liked": liked}


def get_like_response(POST):
    return get_response_from_post(Main, POST, 'like')


def get_listing_response(post):
    request = webapp2.Request.blank('/getListings', POST=post)
    response = request.get_response(Main.app)
    if response.body and (response.status_int == success):
        return json.loads(response.body)['listings'], response.status_int
    elif response.body:
        return json.loads(response.body), response.status_int
    else:
        return None, response.status_int
