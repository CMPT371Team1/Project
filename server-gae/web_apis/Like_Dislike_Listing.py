import os
from extras.Utils import *
from extras.Check_Invalid import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User

import sys
from API_NAME import like_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class LikeDislikeListing(webapp2.RequestHandler):
    """
    LikeDislikeListing class is used to respond to request to like api.
    The post method in this class is used to like or dislike the listing.
    Post:
        @pre-cond: Expecting keys to be listingId, userId and liked.
                   listingId and userId are supposed to be integers and
                   correspond to valid user and listing. liked
                   is either "True" or "False".
        @post-cond: A favorite object with provided listingId and userId is
                    created in the database if it doesn't exist before, or
                    update the liked field if it exists.
        @return-api: nothing.
    """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(like_listing_api, self.request.POST,
                                 self.response)

        if not valid:
            return

        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: 'Listing not authorized'
            }
            write_error_to_response(self.response, error,
                                    unauthorized_access)
            return

        liked = convert_to_bool(values['liked'])
        user_id = int(values['userId'])
        listing_id = int(values['listingId'])

        # make sure that the owner can't like his/her own listing
        listing_owner_id = listing.userId
        if listing_owner_id == user_id:
            error = {
                unallowed_liked['error']: 'Listing can\'t be liked by owner'
            }
            write_error_to_response(self.response, error,
                                    processing_failed)
            return

        # check if the favorite object exists
        favorite = Favorite.query(Favorite.userId == user_id,
                                  Favorite.listingId == listing_id).get()
        if favorite is None:
            favorite = Favorite(userId=user_id, listingId=listing_id, liked=liked)
            favorite.put()
        else:  # if the favorite object does exist
            favorite_liked = favorite.liked
            if liked:
                # user want to like the list
                if favorite_liked:
                    # return duplicate error
                    error = {
                        duplicated_liked['error']: 'The listing is already liked'
                    }
                    write_error_to_response(self.response, error,
                                            processing_failed)
                    return

            else:
                # user want to unlike the list
                if not favorite_liked:
                    # return error
                    error = {
                        duplicated_liked['error']: 'The listing is already disliked'
                    }
                    write_error_to_response(self.response, error,
                                            processing_failed)
                    return

                # change the liked field to be false
                favorite.liked = False
            favorite.put()

        # return successfully
        write_success_to_response(self.response, {})
