from __future__ import absolute_import

import os
import sys
import unittest

import Main
import extras.Error_Code as Error_Code
from models.Listing import Listing
from web_apis.Create_User import *
from API_NAME import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestEditListing(unittest.TestCase):
    """
        test case 1: missing input
        test case 2: missing key-value pair
        test case 3: unrecognized key
        test case 4: the editor, which is not the owner, cannot edit the listing
        test case 5: invalid userId and listingId
        test case 6: unauthorized userId and listingId
        test case 7: input with invalid fields
        test case 8: correct input

    """
    def setUp(self):
        setup_testbed(self)

        # create a user as well as a listing that the user owns
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        owner = users[0]
        self.ownerId = owner['userId']
        self.token = owner['authToken']

        listing_info = create_random_listing(self.ownerId, self.token)
        listing_info['isPublished'] = 'False'

        response, response_status = get_create_listing_response(listing_info)

        assert response_status == success

        output = response
        self.listingId = output["listingId"]

        # now create a new user as an editor
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        editors = users[0]
        self.editorId = editors['userId']
        self.editorToken = editors['authToken']

    def test_missing_input(self):
        res_value, status = get_response(get_post_dictionary("", "", "", {}))

        self.assertEqual(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error'],
                           Error_Code.missing_token['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_missing_key_value(self):
        change_values = {
                "province": "",
                "city": "   ",
                "bathrooms": "",
                "description": "  ",
        }

        res_value, status = get_response(get_post_dictionary
                                         (self.ownerId, self.listingId,
                                          self.token, change_values))

        self.assertEqual(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_province['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_description['error']]

        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_unrecognized_key(self):
        change_values = { "unrecognizedKey": "unrecognizedKey"}

        res_value, status = get_response(
            get_post_dictionary(self.ownerId, self.listingId,
                                self.token, change_values))

        self.assertEqual(status, unrecognized_key["status"])
        error_expected = Error_Code.unrecognized_key['error']
        self.assertTrue(error_expected in res_value)

    def test_listing_auth(self):
        change_values = {"bathrooms": 10}

        res_value, status = get_response(
            get_post_dictionary(self.editorId, self.listingId, self.editorToken,
                                change_values))
        self.assertEquals(status, not_authorized['status'])
        error_expected = Error_Code.not_authorized['error']
        self.assertTrue(error_expected in res_value)

    def invalid_user_id(self):
        change_values = {"bathrooms": 10}
        res_value, status = get_response(
            get_post_dictionary("invalidUserId", "invalidUserId",
                                self.token, change_values))

        self.assertEquals(status, missing_invalid_parameter)
        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.invalid_listing_id['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_unauthorized_userid_listing_id(self):
        change_values = {"bathrooms": 10}
        res_value, status = get_response(
            get_post_dictionary(1111111, 4444444, self.token, change_values))

        self.assertEquals(status, not_authorized['status'])
        error_expected = Error_Code.not_authorized['error']
        self.assertTrue(error_expected in res_value)

    def test_invalid_fields(self):
        change_values = { "bedrooms": "supposed to be a number",
                          "squareFeet": "supposed to be a number",
                          "bathrooms": "supposed to be a number",
                          "price": "supposed to be a number",
                          "isPublished": "supposed to be a boolean",
                          "city": "Regina",
                          "address": "312 Summer Place",
                          "thumbnailImageIndex": "supposed to be a number"
                          }

        res_value, status = get_response(
            get_post_dictionary(self.ownerId, self.listingId, self.token,
                                change_values))

        self.assertEquals(status, missing_invalid_parameter)

        errors_expected = [Error_Code.invalid_bedrooms['error'],
                           Error_Code.invalid_square_feet['error'],
                           Error_Code.invalid_bathrooms['error'],
                           Error_Code.invalid_price['error'],
                           Error_Code.invalid_thumbnail_image_index['error'],
                           Error_Code.invalid_published['error']]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_correct_input(self):
        change_values = {"bedrooms": "4",
                         "squareFeet": "1500",
                         "bathrooms": "5",
                         "price": "2050000",
                         "isPublished": "True",
                         "city": "Regina",
                         "address": "312 Summer Place",
                         "thumbnailImageIndex": 1
                         }

        res_value, status = get_response(
            get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))
        self.assertEquals(status, success)
        listing_changed = Listing.get_by_id(self.listingId)
        self.assertEquals(listing_changed.bedrooms,
                          int(change_values['bedrooms']))
        self.assertEquals(listing_changed.squareFeet, int(change_values['squareFeet']))
        self.assertEquals(listing_changed.bathrooms,
                          float(change_values['bathrooms']))
        self.assertEquals(listing_changed.price, int(change_values['price']))
        self.assertEquals(str(listing_changed.isPublished),
                          change_values['isPublished'])
        self.assertEquals(listing_changed.city, change_values['city'])
        self.assertEquals(listing_changed.address, change_values['address'])
        self.assertEquals(listing_changed.thumbnailImageIndex,
                          int(change_values['thumbnailImageIndex']))

    def test_unpublishing_input(self):
        change_values = {"isPublished": "Fals e"}
        res_value, status = get_response(
            get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))
        self.assertEquals(status, success)
        listing_changed = Listing.get_by_id(self.listingId)
        self.assertEquals(str(listing_changed.isPublished),
                          change_values['isPublished'])

    def test_publish_unpublished_input_with_missing_fields(self):
        listing_info = create_random_listing(self.ownerId, self.token)
        listing_info['isPublished'] = 'False'
        del listing_info['description']
        del listing_info['bedrooms']
        del listing_info['bathrooms']
        del listing_info['thumbnailImageIndex']
        del listing_info['images']
        del listing_info['address']
        del listing_info['squareFeet']
        del listing_info['price']
        del listing_info['longitude']
        del listing_info['latitude']
        del listing_info['postalCode']
        del listing_info['city']
        del listing_info['province']

        request = webapp2.Request.blank('/createListing',
                                        POST=listing_info)
        response = request.get_response(Main.app)
        output = json.loads(response.body)
        listingId2 = output["listingId"]

        change_values = {"isPublished": "True"}
        res_value, status = get_response(
            get_post_dictionary(self.ownerId, listingId2, self.token,
                                change_values))

        self.assertEquals(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_bedrooms['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_description['error'],
                           Error_Code.missing_image['error'],
                           Error_Code.missing_image_index['error'],
                           Error_Code.missing_address['error'],
                           Error_Code.missing_square_feet['error'],
                           Error_Code.missing_price['error'],
                           Error_Code.missing_longitude['error'],
                           Error_Code.missing_latitude['error'],
                           Error_Code.missing_postal_code['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_province['error']]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_post_dictionary(user_id, listing_id, token, change_values):
    return {"userId": user_id, "listingId": listing_id, "authToken": token,
            "changeValues": json.dumps(change_values)}


def get_response(post):
    return get_response_from_post(Main, post, edit_listing_api)


def get_listing_response(post):
    return get_response_from_post(Main, post, get_listing_api)


def get_create_listing_response(post):
    return get_response_from_post(Main, post, create_listing_api)
