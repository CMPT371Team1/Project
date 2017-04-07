from models.Listing import Listing
from models.User import User
from extras.Check_Invalid import *
import sys
import os
from extras.Utils import *
from API_NAME import create_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class CreateListing(webapp2.RequestHandler):
    """
    Post:
        @pre-cond: Expecting keys to be price, squareFeet, bedrooms,
                   bathrooms, description, images, thumbnailImageIndex,
                   city, address, province, userId, isPublished. If any
                   of these is not present an appropriate error and
                   status code 400 is returned.
                   There's a few fields which are supposed to be integer:
                   bedrooms, squareFeet, price, userId and thumbnailImageIndex;
                   There's a field that's supposed to be a float: bathrooms;
                   There's a field that's supposed to be a bool: isPublished
        @post-cond: A listing is created in the database
        @return-api: A listing with provided information is created in the
                    database. ListingId is returned as an response
                    object.

    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(create_listing_api, self.request.POST,
                                 self.response, True)
        if not valid:
            return

        is_published = convert_to_bool(values["isPublished"])
        if not is_published:
            listing = Listing(userId=int(values['userId']), isPublished=False)
            for key in values:
                if key not in ["authToken", "listingId", "userId", "isPublished"]:
                    if key == 'images':
                        listing.images = format_images_from_request(values)
                    elif key == 'province':
                        listing.province = scale_province(str(values['province']))
                    else:
                        listing.set_property(key, values[key])
            listing.put()
            listing.set_property('listingId', listing.key.id())
            listing.put()
            write_success_to_response(self.response,
                                      {'listingId': listing.listingId})
            return

        # create a published listing
        error_keys = listing_keys
        errors, values = keys_missing(error_keys, self.request.POST)
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        values['province'] = scale_province(str(values['province']))

        # all set
        format_images_from_request(values)

        listing = Listing(userId=int(values['userId']),
                          bedrooms=int(values['bedrooms']),
                          squareFeet=int(values['squareFeet']),
                          bathrooms=float(values['bathrooms']),
                          price=int(values['price']),
                          description=values['description'],
                          isPublished=True, province=values['province'],
                          city=values['city'],
                          address=values['address'], images=values['images'],
                          longitude=float(values['longitude']),
                          latitude=float(values['latitude']),
                          thumbnailImageIndex=int(
                              values['thumbnailImageIndex']),
                          postalCode=values['postalCode'])
        listing.put()
        listing.set_property('listingId', listing.key.id())
        listing.put()
        write_success_to_response(self.response,
                                  {'listingId': listing.listingId})


def format_images_from_request(values):
    values['images'] = json.loads(values['images'])
    values['images'] = [str(image) for image in values['images']]
    return values['images']

