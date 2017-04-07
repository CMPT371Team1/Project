from __future__ import absolute_import

import os
import unittest
import webapp2

from extras.Check_Invalid import *
from extras.Random_Models import *
from API_NAME import *
from extras.Required_Fields import *
from extras.Base_Handler import BaseHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestRequiredFields(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)
        self.response = webapp2.Response()

    def test_sign_in_missing_email(self):
        missing_email_post = {"password": 123}
        valid, values = \
            check_required_valid(sign_in_api, missing_email_post, self.response)

        self.assertFalse(valid)
        self.assertIsNone(values)
        response_body, response_status = \
            get_dictionary_from_response(self.response)
        self.assertEqual(response_status, missing_invalid_parameter)
        self.assertTrue(are_two_lists_same(response_body.keys(),
                                           [missing_email["error"]]))


def get_dictionary_from_response(response):
    if response.body:
        json_body = json.loads(response.body)
        if json_body:
            dictionary = {str(key): json_body[str(key)] for key in
                          json_body}
            return dictionary, response.status_int
    return None, response.status_int
