import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *
from extras.utils import *
from models.User import User
from extras.User_Auth import user_required
from webapp2_extras import auth


class EditUser(BaseHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
    """
    def get(self):
        self.render_template('../webpages/Edit_User.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        # check if user id and token are present
        error_keys = ['changeValues', 'userId', 'authToken']
        errors, values = keys_missing(error_keys, self.request.POST)

        if len(errors) != 0:
            write_error_to_response(self, errors, missing_invalid_parameter_error)
            return

        change_values = json.loads(values['changeValues'])
        if len(change_values) == 0:

            write_error_to_response(self, {nothing_requested_to_change['error']:
                                            "Nothing requested to change"},
                                    nothing_requested_to_change['status'])
            return
        valid_user = self.user_model.validate_token(int(values["userId"]),"auth",
                                        values["authToken"])
        if not valid_user:
            write_error_to_response(self, {not_authorized['error']:
                                    "not authorized to chnage user"},
                                    not_authorized['status'])
            return

        if "password" in change_values.keys():
            write_error_to_response(self, {password_cant_be_changed['error']:
                                "Please don't change password using edit user"},
                                    password_cant_be_changed['status'])
            return

        if any(key not in ["phone1", "phone2", "email", "province", "city",
                "firstName", "lastName"] for key in change_values.keys()):
            write_error_to_response(self, {unrecognized_key['error']:
                                    "Unrecognized key found"},
                                    unrecognized_key['status'])
            return

        invalid = key_validation(change_values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter_error)
            return

        user = User.get_by_id(int(values["userId"]))
        #todo Edit the user



















