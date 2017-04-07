import os
from extras.Utils import *
from extras.Check_Invalid import *
from models.FacebookUser import FacebookUser
from models.User import User
import sys
from extras.Base_Handler import BaseHandler
from API_NAME import fb_login_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class FacebookLogin(BaseHandler):
    """
    FacebookLogin class is used to respond to request to signInWithFacebook api.
    The post method in this class is used to sign in the user by validating
    the facebook id, and creating a token for the user.
    POST
        @pre-cond: Expecting keys to be fbId
                   User with provided fbId should be present in the
                   database.
        @post-cond: A token is generated which will allow user to login.
        @return-api: A valid Token, with all the user details is returned in
                     response.
    """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(fb_login_api, self.request.POST, self.response)

        if not valid:
            return

        # find the correct user with userId
        fb_query = FacebookUser.query().filter(
            FacebookUser.fb_id == int(values["fbId"])).fetch(keys_only=True)

        if len(fb_query) == 0:
            write_error_to_response(self.response, {
                invalid_fb_id["error"]: "Fb ID not found"
            }, invalid_fb_id["status"])
            return

        assert len(fb_query) == 1
        fb_entry_id = fb_query[0].integer_id()
        fb_entry = FacebookUser.get_by_id(fb_entry_id)
        fb_user = User.get_by_id(fb_entry.user_id)
        token = self.user_model.create_auth_token(fb_entry.user_id)
        user_dict = {'token': token,
                     'userId': fb_user.get_id(),
                     'email': fb_user.email,
                     'firstName': fb_user.first_name,
                     'lastName': fb_user.last_name,
                     'phone1': fb_user.phone1,
                     'phone2': fb_user.phone2,
                     'city': fb_user.city,
                     'province': fb_user.province}

        write_success_to_response(self.response, user_dict)
