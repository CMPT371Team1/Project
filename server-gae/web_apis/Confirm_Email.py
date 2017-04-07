# when websites send us an activation link after a registration,
# the url usually contain their equivalent of signup tokens.
import logging
from extras.Base_Handler import BaseHandler


class VerificationHandler(BaseHandler):
    """
    Get: Verifies a user when they click on their email verifications link. A
    get request specifying this is sent to this class.
        @pre-cond: User  have a valid signup token userID
        @post-cond: User is verified.
        @return: None
    """
    def get(self, *args, **kwargs):
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']
        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token,
                                                     'signup')
        if not user:
            logging.info(
                'Could not find any user with id "%s" signup token "%s"',
                user_id, signup_token)
            self.abort(404)

        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        # remove signup token, we don't want users
        # to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), signup_token)

        if not user.verified:
            user.verified = True
            user.put()
            assert user.verified
            return

        else:
            assert user.verified
            assert(verification_type is not None)
            logging.info('verification type not supported.')
            self.abort(404)
