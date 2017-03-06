import os
from extras.utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
import sys
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class LikeDislikeListing(webapp2.RequestHandler):
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
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):

        self.render_template('../webpages/Like_dislike_listing.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        error_keys = ['userId', 'listingId', 'liked']

        # check if there's any missing field, if so, just return to the user what all is missing
        errors, values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        # if not, then go ahead and check validity
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        # check validity for integer fields (userId and listingId) and a boolean field (isPublished)
        invalid = key_validation(values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter)
            return

        # find the correct user with userId
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            write_error_to_response(self.response, error,
                                    unauthorized_access)
            return

        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: 'Listing not authorized'
            }
            write_error_to_response(self.response, error,
                                    unauthorized_access)
            return

        liked = True if values['liked'] in ['true', "True", "TRUE", '1', "t", "y", "yes"] else False

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

        # Next, check if the favorite object already exists
        # if it already exists, check the user input liked
        #   if liked == true, then it means the user want to like the list
        #       if the liked field in the object is true, return error
        #       if the liked field in the object is false, change it to true
        #   if liked == false, then it means the user want to unlike the list
        #       if the liked field in the object is false, then return error
        #       if the liked field in the object is true, change it to false
        # if the favorite object doesn't exist
        #   create a new favorite object with liked input value

        # check if the favorite object exists
        favorite = Favorite.query(Favorite.userId == user_id,
                                  Favorite.listingId == listing_id).get()
        if favorite is None:
            # TODO: do we need to make sure that the liked input is true when creating the favorite object?
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

                # if everything is correct, change the liked field to be true
                favorite.liked = True

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
