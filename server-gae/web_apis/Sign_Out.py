from extras.Utils import *
import sys
from models import User
sys.path.append("../")
from extras.Base_Handler import BaseHandler
from API_NAME import sign_out_api
from extras.Required_Fields import check_required_valid


class SignOut(BaseHandler):
    """
    SignOut class is used to respond to request to signOut api. The post method
    in this class is used to sign out the user by invalidating the token.
    Post:
        @pre-cond: Expecting keys to be userId and authToken.
                   User with provided userId should be present in the database.
                   authToken should be valid for given userId.
        @post-cond: authToken provided is not valid anymore.
        @return-api: Nothing
    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(sign_out_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        token = values['authToken']

        assert token is not None

        self.user_model.delete_auth_token(int(values['userId']), token)
        write_success_to_response(self.response, {})
