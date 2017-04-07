import sys
sys.path.append('../')
import logging
from extras.Base_Handler import BaseHandler
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from extras.Check_Invalid import *
from API_NAME import *
from extras.Required_Fields import check_required_valid


class ChangePassword(BaseHandler):
    """
    Post:
        @pre-cond: Expecting keys to be old_password,
                   new_password, and confirmed_password.

        @post-cond: On success, a user's password is changed in the database.

        @:return:   A new token and code 200 on success, otherwise,
                    an appropriate error message and code.

    """
    def post(self):
        setup_post(self.response)
        # For each required field, making sure it is non-null, non-empty
        # and contains more than space characters

        valid, values = \
            check_required_valid(change_password_api, self.request.POST,
                                 self.response)

        if not valid:
            return

        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'Invalid credentials'
            }
            write_error_to_response(self.response, error,
                                    not_authorized['status'])
            logging.info(
                'Sign-in-with-token failed for user %s because of %s',
                int(values['userId']))
            return

        try:
            # attempt to get the current user by the old password. Will throw an
            # exception if the password or e-mail are unrecognized.
            user_dict = self.auth.get_user_by_password(
                user.email, values['oldPassword'], remember=True,
                save_session=True)
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         values['userId'], type(e))
            error = {
                not_authorized['error']: 'Invalid credentials'
            }
            write_error_to_response(self.response, error,
                                    not_authorized['status'])
            return


        # Get a new token
        token = user_dict['token']
        self.user_model.delete_auth_token((values['userId']), token)
        token = self.user_model.create_auth_token((values['userId']))

        if not is_valid_password(values['newPassword']):
            error = {
                password_not_strong['error']: 'Password not strong enough'
            }
            write_error_to_response(self.response, error,
                                    password_not_strong['status'])
            return

        if values['newPassword'] != values['confirmedPassword']:
            error = {
                password_mismatch['error']:
                    'Password and confirmed password do not match'
            }
            write_error_to_response(self.response, error,
                                    password_mismatch['status'])
            return

        if values['newPassword'] == values['oldPassword']:
            error = {
                new_password_is_the_same_as_old['error']:
                    'New password is same as the old password'
            }
            write_error_to_response(self.response, error,
                                    new_password_is_the_same_as_old['status'])
            return

        User.set_password(user, values['newPassword'])

        user_dict = {'authToken': token}

        write_success_to_response(self.response,user_dict)
