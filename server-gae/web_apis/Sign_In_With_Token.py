from extras.Utils import *
from models.User import *
import sys
sys.path.append('../')
from extras.Base_Handler import BaseHandler
from API_NAME import sign_in_token_api
from extras.Required_Fields import check_required_valid


class SignInWithToken(BaseHandler):
    """
    POST
        @pre-condition: Post has email and token
        @post-condition: None
        @return-api: The user's token
    """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(sign_in_token_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        assert values['authToken'] is not None and values['userId'] is not None

        user = (User.get_by_auth_token(int(values['userId']), values['authToken'], subject='auth'))[0]

        assert user is not None

        self.user_model.delete_auth_token(values['userId'], values['authToken'])
        token = self.user_model.create_auth_token(values['userId'])

        assert token is not values['authToken']
        user_dict = {'authToken': token,
                     'userId': user.get_id(),
                     'email': user.email,
                     'firstName': user.first_name,
                     'lastName': user.last_name,
                     'phone1': user.phone1,
                     'phone2': user.phone2,
                     'city': user.city,
                     'province': user.province}
        write_success_to_response(self.response, user_dict)
