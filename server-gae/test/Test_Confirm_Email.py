from __future__ import absolute_import
from API_NAME import create_user_api
from extras.Random_Models import *
import os
import sys
import unittest
import Main
from extras.Utils import *
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestConfirmEmail(unittest.TestCase):
    """
    These are test, being tested
    Different kinds of empty strings and null values
    Test invalid phone 1
    Test invalid phone 2
    Test password mismatch
    Test not strong password
    Test all valid fields
    """
    def setUp(self):
        setup_testbed(self)

    def test_create_user_with_email_confirmation(self):
        random_user = create_random_user()
        response_body, status_int = get_response_from_post(Main, random_user,
                                                           create_user_api)
        self.assertEquals(status_int, success)
        self.assertTrue("authToken" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))

        messages = self.mail_stub.get_sent_messages(to=user_saved.email)

        self.assertEqual(1, len(messages))
        self.assertEqual(user_saved.email, messages[0].to)

    def tearDown(self):
        self.testbed.deactivate()
