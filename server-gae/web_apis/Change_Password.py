import sys
sys.path.append('../')
import logging
from extras.Base_Handler import BaseHandler
from models.User import *
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from extras.utils import *
from API_NAME import *
from extras.api_required_fields import check_required_valid


class ChangePassword(BaseHandler):
    """
    lass containing the get and post for Change Password.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be old_password,
                   new_password, and confirmed_password.

        @post-cond: On success, a user's password is changed in the database.

        @:return:   A new token if success with code 200, otherwise,
                    an appropriate error message and code.

    """

    def options(self, *args, **kwargs):
        setup_api_options(self)


    def get(self):
        self.render_template('../webpages/Change_Password.html')

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
                not_authorized['error']: "Invalid credentials"
            }
            write_error_to_response(self.response, error,
                                    not_authorized['status'])
            return

        if user is None:
            error = {
                not_authorized['error']: "Invalid credentials"
            }
            write_error_to_response(self.response, error,
                                    not_authorized['status'])
            logging.info(
                'Sign-in-with-token failed for user %s because of %s',
                int(values['userId']))
            return

        # Get a new token
        token = user_dict['token']
        self.user_model.delete_auth_token((values['userId']), token)
        token = self.user_model.create_auth_token((values['userId']))

        if not is_valid_password(values['newPassword']):
            error = {
                password_not_strong['error']: "Password not strong enough"
            }
            write_error_to_response(self.response, error,
                                    password_not_strong['status'])
            return

        if values['newPassword'] != values['confirmedPassword']:
            error = {
                password_mismatch['error']:
                    "Password and confirmed password do not match"
            }
            write_error_to_response(self.response, error,
                                    password_mismatch['status'])
            return

        if values['newPassword'] == values['oldPassword']:
            error = {
                new_password_is_the_same_as_old['error']:
                    "New password is same as the old password"
            }
            write_error_to_response(self.response, error,
                                    new_password_is_the_same_as_old['status'])
            return

        User.set_password(user, values['newPassword'])

        try:
            # This will throw an exception if the password is wrong, which will
            # only happen if set_password failed.
            user_dict = self.auth.get_user_by_password(
                user.email, values['newPassword'], remember=True,
                save_session=True)
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            # set_password failed. This should never happen
            assert False
        # self.auth.store.delete_auth_token(user['userId'], user['token'])
        user_dict = {'authToken': token}

        write_success_to_response(self.response,user_dict)
