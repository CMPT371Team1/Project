import logging
import json
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from Base_Handler import BaseHandler
from Error_Code import *


class SignIn(BaseHandler):
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
        user_email = self.request.POST.get('email')
        if user_email is None:
            message[missing_email['error']] = "Missing user email"
        password = self.request.POST.get('password')
        if password is None:
            message[missing_password["error"]] = "Missing password"

        if len(message.keys()) != 0:
            self.response.write(json.dumps(message))
            self.response.set_status(missing_invalid_parameter_error)
            return

        assert user_email is not None and password is not None
        try:
            user = self.auth.get_user_by_password(
                user_email, password, remember=True, save_session=True)
            #This should be changed later so that user email is in the database.
            user_dict = {'token': user['token'],
                         'userId': user['user_id'],
                         'email': user_email,
                         'firstName': user['first_name'],
                         #'lastName': user['last_name'],
                         'phone1': user['phone1'],
                         'phone2': user['phone2'],
                         'city': user['city'],
                         'province': user['province']}
            self.response.out.write(json.dumps(user_dict))
            self.response.set_status(success)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         user_email, type(e))
            error = json.dumps(not_authorized["error"])
            self.response.write(error)
            self.response.set_status(not_authorized['status'])

    def _serve_page(self, failed=False):
        user_email = self.request.get('email')
        params = {
            'user_email': user_email,
            'failed': failed
        }
        self.response.write("Failed")
        self.render_template('Sign_In.html', params)