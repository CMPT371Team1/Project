from google.appengine.api import mail
from extras.Base_Handler import BaseHandler
from extras.Utils import *
from extras.Check_Invalid import *
from models.FacebookUser import FacebookUser
from models.Favorite import Favorite
from models.Listing import Listing
from models.Message import Message
from models.User import User
from webapp2_extras.appengine.auth.models import UserToken, Unique
from extras.Test_Databse import *
import Main


class InitializeDB(BaseHandler):
    """
    InitializeDB class is used to reinitialize the database with information
    provided in Test_Database.py. Please use this with caution, this exists
    only for testing purposes. A better way has to found in order to overcome
    this issue.
    !!!NOTE: This class should only be used on testing database!!!
    Post:
        @pre-cond: None
        @post-cond: Database is reset to have data defined in Test_Database.py
        @return-api: nothing
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)


    def post(self):
        models_list = [FacebookUser, Favorite, Listing, Message, User,
                       UserToken,
                       Unique]

        for model in models_list:
            for member in model.query().fetch():
                print("deleting" + str(member))
                member.key.delete()
        responses = []
        for user in users:
            response, _ = get_response_from_post(Main, user, 'createUser')
            responses.append(response)

        number_of_responses = len(responses)
        for i in range(len(listings_published)):
            listing = listings_published[i]
            listing["userId"] = responses[i % number_of_responses]["userId"]
            listing["authToken"] = responses[i % number_of_responses][
                "authToken"]
            get_response_from_post(Main, listing, 'createListing')

        for i in range(len(listing_unpublished)):
            listing = listing_unpublished[i]
            listing["userId"] = responses[i % number_of_responses]["userId"]
            listing["authToken"] = responses[i % number_of_responses][
                "authToken"]
            get_response_from_post(Main, listing, 'createListing')

        create_dummy_listings_for_testing(Main, random_listings, random_users)
        write_success_to_response(self.response, {})
