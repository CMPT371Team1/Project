from __future__ import absolute_import
import os
import sys
import unittest
from extras.Check_Invalid import *
import Main
from models.Listing import Listing
from web_apis.Create_User import *
from API_NAME import create_listing_api
from extras.Random_Models import *
sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestCreateListing(unittest.TestCase):
    """
        test case 1: empty object as input
        test case 2
        checking if all error codes are received, if empty code is sent
        test case 3
        checking if all error codes are received, if all user inputs are spaces
        test case 4: missing userId and token
        test case 5: invalid userId
        test case 6: invalid numeric fields
        test case 7: correct input
        test case 8: invalid bathroom
        test case 9: empty images
        test case 10: success without optional fields for unpublished listings
        test case 11: missing isPublished field
        test case 12: success with optional fields for unpublished listings

    """
    def setUp(self):
        setup_testbed(self)
        users = create_dummy_users_for_testing(Main, 1)
        self.assertEquals(len(users), 1)
        self.user = users[0]

    def test_empty_input(self):
        empty_input = {}
        response, response_status = get_listing_api_response(empty_input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_published['error'],
                           missing_token['error']]

        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_empty_fields(self):
        empty_fields_input = {'userId': '',
                 'authToken': '',
                 'bedrooms': '',
                 'squareFeet': '',
                 'bathrooms': '',
                 'price': '',
                 'description': '',
                 'isPublished': '',
                 'province': '',
                 'city': '',
                 'address': '',
                 'thumbnailImageIndex': '',
                 'longitude': '',
                 'latitude': '',
                 'images': '',
                 'postalCode': ''
                 }
        response, response_status = get_listing_api_response(empty_fields_input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_published['error'],
                           missing_token['error']]

        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_multiple_spaces_input(self):
        input = {'userId': '      ',
                 'authToken': '      ',
                 'bedrooms': '       ',
                 'squareFeet': '        ',
                 'bathrooms': '      ',
                 'price': '        ',
                 'description': '      ',
                 'isPublished': '      ',
                 'province': '       ',
                 'city': '       ',
                 'address': '      ',
                 'longitude': '   ',
                 'latitude': '   ',
                 'thumbnailImageIndex': '      ',
                 'images': '    ',
                 'postalCode': '   ',
                 }

        response, response_status = get_listing_api_response(input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_published['error'],
                           missing_token['error']]

        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_missing_userId_and_token(self):
        missing_input = create_random_listing('', '')

        response, response_status = get_listing_api_response(missing_input)

        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_token['error']]

        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_invalid_user_id(self):
        input = create_random_listing('1111', 'sfasdtr54523df')

        response, response_status = get_listing_api_response(input)
        self.assertEquals(response_status, unauthorized_access)

        errors_expected = [not_authorized['error']]
        error_keys = [str(x) for x in response]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_invalid_numeric_field(self):
        input = create_random_listing('supposed to be int', 'random token')
        input['bedrooms'] = 'supposed to be int'
        input['squareFeet'] = 'supposed to be int'
        input['bathrooms'] = 'supposed to be float'
        input['price'] = 'supposed to be int'
        input['thumbnailImageIndex'] = 'supposed to be int'
        input['longitude'] = 'supposed to be float'
        input['latitude'] = 'supposed to be float'
        input['postalCode'] = 'supposed to be float'

        response, response_status = get_listing_api_response(input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [invalid_user_id['error'],
                           invalid_bedrooms['error'],
                           invalid_square_feet['error'],
                           invalid_bathrooms['error'],
                           invalid_price['error'],
                           invalid_longitude['error'],
                           invalid_latitude['error'],
                           invalid_postal_code['error'],
                           invalid_thumbnail_image_index['error']
                           ]

        error_keys = [str(x) for x in response]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_correct_input(self):
        correct_input = create_random_listing(self.user['userId'], self.user['authToken'])
        correct_input['bathrooms'] = 5.5
        correct_input['isPublished'] = 'True'

        response, response_status = get_listing_api_response(correct_input)

        self.assertEquals(response_status, success)

        output = response
        self.assertTrue('listingId' in output)

        listing_created = Listing.get_by_id(int(output['listingId']))
        self.assertEquals(listing_created.bedrooms, int(correct_input['bedrooms']))
        self.assertEquals(listing_created.squareFeet, int(correct_input['squareFeet']))
        self.assertEquals(listing_created.bathrooms, float(correct_input['bathrooms']))
        self.assertEquals(listing_created.price, int(correct_input['price']))
        self.assertEquals(listing_created.description, correct_input['description'])
        self.assertEquals(str(listing_created.isPublished), correct_input['isPublished'])
        self.assertEquals(listing_created.province, correct_input['province'])
        self.assertEquals(listing_created.city, correct_input['city'])
        self.assertEquals(listing_created.address, correct_input['address'])
        self.assertEquals(listing_created.thumbnailImageIndex, int(correct_input['thumbnailImageIndex']))
        self.assertEquals(listing_created.images, json.loads(correct_input['images']))

    def test_invalid_bathroom_input(self):
        invalid_bathroom_input = create_random_listing(self.user['userId'], self.user['authToken'])
        invalid_bathroom_input['bathrooms'] = 5.25
        response, response_status = get_listing_api_response(invalid_bathroom_input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [invalid_bathrooms['error']]

        error_keys = [str(x) for x in response]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_empty_images_input(self):
        empty_image_input = create_random_listing(self.user['userId'], self.user['authToken'])
        empty_image_input['isPublished'] = 'true'
        empty_image_input['images'] = json.dumps([])
        response, response_status = get_listing_api_response(empty_image_input)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_image['error']]

        error_keys = [str(x) for x in response]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_correct_create_unpublished_listing(self):
        correct_input = create_random_listing(self.user['userId'], self.user['authToken'])
        correct_input['isPublished'] = 'False'
        del correct_input['bedrooms']
        del correct_input['bathrooms']
        del correct_input['description']
        del correct_input['images']
        del correct_input['address']
        del correct_input['squareFeet']
        del correct_input['price']
        response, response_status = get_listing_api_response(correct_input)

        self.assertEquals(response_status, success)

        output = response
        self.assertTrue('listingId' in output)

        listing_created = Listing.get_by_id(int(output['listingId']))
        self.assertEquals(None, listing_created.bedrooms)
        self.assertEquals(None, listing_created.bathrooms)
        self.assertEquals(None, listing_created.description)
        self.assertEquals([], listing_created.images)
        self.assertEquals(None, listing_created.address)
        self.assertEquals(None, listing_created.squareFeet)
        self.assertEquals(None, listing_created.price)

    def test_missing_is_published(self):
        correct_input = create_random_listing(self.user['userId'], self.user['authToken'])
        del correct_input['isPublished']
        response, response_status = get_listing_api_response(correct_input)

        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [missing_published['error']]

        error_keys = [str(x) for x in response]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_success_with_empty_optional_fields_when_isPublished_is_false(self):
        correct_input = create_random_listing(self.user['userId'], self.user['authToken'])

        correct_input['isPublished'] = 'False'
        response, response_status = get_listing_api_response(correct_input)

        self.assertEquals(response_status, success)

        output = response
        self.assertTrue('listingId' in output)

        listing_created = Listing.get_by_id(int(output['listingId']))
        self.assertEquals(correct_input['bedrooms'], str(listing_created.bedrooms))
        self.assertEquals(float(correct_input['bathrooms']), listing_created.bathrooms)
        self.assertEquals(correct_input['description'], listing_created.description)
        self.assertEquals(correct_input['address'], listing_created.address)
        self.assertEquals(correct_input['squareFeet'], str(listing_created.squareFeet))
        self.assertEquals(correct_input['price'], str(listing_created.price))

    def tearDown(self):
        self.testbed.deactivate()


def get_listing_api_response(input_dictionary):
    return get_response_from_post(Main, input_dictionary, create_listing_api)
