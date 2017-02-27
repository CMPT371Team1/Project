import logging
import json
import sys

from extras.utils import *

sys.path.append("../")
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *


class SignInWithToken(BaseHandler):
    """
    The implementation above renders the login page when the request
    comes via GET and processes the credentials upon POST. When authentication
    fails it renders the login page and passes the username to the template so
    that the corresponding field can be pre-filled.

    @pre-condition: Post has email and password
    @post-condition:
    @return-api:
    """

    def get(self):
        self._serve_page()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        message = {}
        token = self.request.POST.get('token')
        if token is None:
            message[missing_token['error']] = "Missing user token"

        user_id = self.request.POST.get('userId')
        if user_id is None:
            message[missing_user_id['error']] = "Missing user id"

        if len(message.keys()) != 0:
            write_error_to_response(self, message,
                         missing_invalid_parameter_error)
            return

        assert token is not None
        try:
            #Todo This is all wrong.userId is supposed to be given, and not email.
            user = self.get_by_auth_token(user_id, token, subject='auth')

            user_dict = {'token': user['token'],
                         'userId': user['user_id'],
                         'email': user['email'],
                         'firstName': user['first_name'],
                         'lastName': user['last_name'],
                         'phone1': user['phone1'],
                         'phone2': user['phone2'],
                         'city': user['city'],
                         'province': user['province']}
            self.response.out.write(json.dumps(user_dict))
            self.response.set_status(success)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in-with-token failed for user %s because of %s',
                         user_email, type(e))
            write_error_to_response(self, not_authorized["error"], not_authorized['status'])

    def _serve_page(self, failed=False):
        params = {
            'failed': failed
        }
        self.response.write("Failed")
        self.render_template('../webpages/Sign_In_With_Token.html', params)
