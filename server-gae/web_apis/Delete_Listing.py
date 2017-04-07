import os
from extras.Utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
from extras.Check_Invalid import *
import sys
from API_NAME import delete_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class DeleteListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: userId, authToken and listingId are expected.
                   authToken should be valid.
                   listingId should point to valid listing.
                   userId should be owner of the listing.

        @post-cond: Listing with listingId is removed from the database.
                    Listing is also removed from all favourites.

        @return: Nothing

    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(delete_listing_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        listing = Listing.get_by_id(int(values['listingId']))

        if listing is None:
            error = {
                un_auth_listing['error']: 'Listing not authorized'
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        user_id = int(values['userId'])
        listing_id = int(values['listingId'])

        # make sure that the userId is the owner id of the listing
        listing_owner_id = listing.userId

        if listing_owner_id != user_id:
            error = {not_authorized['error']:
                         "Provided user ID doesn't match the owner id of the listing"}
            write_error_to_response(self.response, error, unauthorized_access)
            return

        # delete all favorites related to this listing
        favorites = Favorite.query(Favorite.listingId == listing_id).fetch()
        if favorites:
            for favorite in favorites:
                favorite.key.delete()

        assert listing is not None

        # delete the listing itself
        listing.key.delete()

        # return successfully
        write_success_to_response(self.response, {})




























