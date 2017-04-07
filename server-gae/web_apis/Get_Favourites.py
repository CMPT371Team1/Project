import sys
from extras.Utils import *
from extras.Check_Invalid import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
from API_NAME import get_favourites_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")


class GetFavourites(webapp2.RequestHandler):
    """
    GetFavourites class is used to respond to request to getFavourites api.
    The post method in this class is used to get all the listings liked by
    the user.
    Post:
        @pre-cond: Expecting keys to be userId and authToken.
                   User with provided userId should be present in the database.
                   authToken should be valid for given userId.
        @post-cond: Nothing
        @return-api: All the listings liked by the user with userId are
                     returned.
    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(get_favourites_listing_api,
                                 self.request.POST, self.response, True)

        if not valid:
            return
        # Get all favorites object that satisfies the filter condition
        favorites = Favorite.query(Favorite.userId == int(values['userId']),
                                   Favorite.liked == True).fetch()

        returned_array = []
        count_listings = 0
        published_favourites = False
        for favorite in favorites:
            fav_listing_id = favorite.listingId
            listing = Listing.get_by_id(fav_listing_id)
            assert listing is not None
            if listing.isPublished:
                published_favourites = True
                count_listings += 1
                template_values = {
                    'listingId': fav_listing_id,
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
                    'images': listing.images,
                    'longitude': listing.longitude,
                    'latitude': listing.latitude,
                    'postalCode': listing.postalCode,
                    'thumbnailImageIndex': listing.thumbnailImageIndex
                }
                returned_array.append(template_values)
            assert (favorites is not None)

        assert (len(returned_array) == count_listings)
        # For the following two asserts, If A then B <==> !A or B
        assert (not (len(returned_array) == 0) or (not published_favourites))
        assert (not (len(returned_array) > 0) or published_favourites)
        assert valid
        # returned_array is either [] or contains as many elements are there
        # are published listings in favourites.
        write_success_to_response(self.response, {"listings": returned_array})
