import os
from extras.Utils import *
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
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be listingId, userId and liked. If any
                   of these is not present an appropriate error and
                   status code 400 is returned.

                   listingId and userId are supposed to be integers, and liked
                   is either "True" or "False".
        @post-cond: A favorite object with provided listingId and userId is created in the
                    database if it doesn't exist before, or update the liked field if it exists.
                    Return nothing.
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
