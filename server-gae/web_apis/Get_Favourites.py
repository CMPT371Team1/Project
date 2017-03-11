import sys
from extras.utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
sys.path.append("../")


class GetFavourites(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  do nothing
    Post:
        @pre-cond: Expecting keys to be userId
        @post-cond: favorite listings that are published
    """
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['userId', 'authToken']

        # check if there's any missing field, if so, just return to the user what all is missing
        errors, values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        # if not, then go ahead and check validity
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        # check validity for integer fields (userId)
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
            write_error_to_response(self.response, error, not_authorized)
            return

        # Check if it is the valid user
        valid_user = user.validate_token(int(values["userId"]),
                                         "auth",
                                         values["authToken"])
        if not valid_user:
            write_error_to_response(self.response, {not_authorized['error']:
                                                        "not authorized to get favourites"},
                                    not_authorized['status'])
            return

        # Get all favorites object that satisfies the filter condition
        favorites = Favorite.query(Favorite.userId == int(values['userId']),
                                   Favorite.liked == True).fetch()

        returned_array = []
        for favorite in favorites:
            fav_listingId = favorite.listingId
            listing = Listing.get_by_id(fav_listingId)

            if listing.isPublished:
                template_values = {
                    'listingId': fav_listingId,
                    'userId': listing.userId,
                    'bedrooms': listing.bedrooms,
                    'squarefeet': listing.squarefeet,
                    'bathrooms': listing.bathrooms,
                    'price': listing.price,
                    'description': listing.description,
                    'isPublished': listing.isPublished,
                    'province': listing.province,
                    'city': listing.city,
                    'address': listing.address,
                    'images': listing.images,
                    'longitude': listing.longitude,
                    'latitude': listing.latitude,
                    'thumbnailImageIndex': listing.thumbnailImageIndex
                }
                returned_array.append(template_values)

        write_success_to_response(self.response, {"listings": returned_array})