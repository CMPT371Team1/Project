import sys
from extras.Utils import *
from extras.Check_Invalid import *
from models.Listing import Listing
from models.User import User
from API_NAME import get_messages_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")


class GetMyListing(webapp2.RequestHandler):
    """
    GetMyListing class is used to respond to request to getMyListing api.
    The post method in this class is used to get all the listings added by
    the provided user.
    Post:
        @pre-cond: Expecting keys to be userId and authToken.
                   User with provided userId should be present in the database.
                   authToken should be valid for given userId.
        @post-cond: Nothing
        @return-api: All the listing of the user with userId are returned.
    """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(get_messages_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        assert values['userId'] is not None
        owner_id = int(values['userId'])

        my_listings = Listing.query(Listing.userId == owner_id).fetch()
        returned_array = []

        for listing in my_listings:
            template_values = {
                'listingId': listing.listingId,
                'userId': listing.userId,
                'bedrooms': listing.bedrooms,
                'squareFeet': listing.squareFeet,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'address': listing.address,
                'longitude': listing.longitude,
                'latitude': listing.latitude,
                'images': listing.images,
                'thumbnailImageIndex': listing.thumbnailImageIndex,
                'postalCode': listing.postalCode
            }
            returned_array.append(template_values)

        write_success_to_response(self.response, {"listings": returned_array})
