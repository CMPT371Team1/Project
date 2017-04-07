import logging

from extras.Utils import *
from extras.Check_Invalid import *
import sys
sys.path.append('../')
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *
from extras.Required_Fields import check_required_valid
from API_NAME import *


class SignIn(BaseHandler):
    """
    SignIn class is used to respond to request to signIn api.
    The post method in this class is used to sign in the user by validating
    the password, and creating a token for the user.
    POST
        @pre-cond: Expecting keys to be userId and password.
                   User with provided userId should be present in the database.
                   password should be valid for given userId.
        @post-cond: A token is generated which will allow user to login.
        @return-api: A valid Token, with all the user details is returned in
                     response.
    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(sign_in_api, self.request.POST, self.response)

        if not valid:
            return

        assert values['email'] is not None and values['password'] is not None
        try:
            # sign in and return user information.
            user = self.auth.get_user_by_password(
                (values['email']).lower(), values['password'], remember=True,
                save_session=True)

            user_dict = {'authToken': user['token'],
                         'userId': user['user_id'],
                         'email': user['email'],
                         'firstName': user['first_name'],
                         'lastName': user['last_name'],
                         'phone1': user['phone1'],
                         'phone2': user['phone2'],
                         'city': user['city'],
                         'province': user['province']}
            write_success_to_response(self.response,user_dict)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         values['email'], type(e))
            error = {
                not_authorized['error']: 'email or password was incorrect'
            }
            write_error_to_response(self.response, error,
                                    not_authorized['status'])
