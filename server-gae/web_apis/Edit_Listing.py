import copy
from extras.Utils import *
import datetime
from models.Listing import Listing
from models.User import User
import sys
import os
from API_NAME import edit_listing_api
from extras.Required_Fields import check_required_valid
from extras.Check_Invalid import *
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class EditListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: listing object  is not null
                   listingId  is an int
                   userId     is an int
                   valuesRequired  is a dict
        @post-cond: if isPublished field changed listing should have all
                    required fields.
        @return: a timestamp of modified date
    """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(edit_listing_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        change_values = json.loads(values['changeValues'])

        # check if there's any unrecognized key presented in changeValues
        if any(key not in listing_keys for key in change_values.keys()):
            error = {unrecognized_key['error']: "Unrecognized key found"}
            write_error_to_response(self.response, error,
                                    unrecognized_key['status'])
            return

        # In order to detect empty field in changeValues keys
        # for example,
        # wrongPairInput = {
        #     "changeValues": {
        #         "province": "",
        #         "city": "   ",
        #         "bathrooms": "",
        #         "description": "  ",
        #     },
        #     "userId": "",
        #     "listingId": ""
        # }
        # we need to go through each field in the dictionary
        change_error_keys = []
        for change_key in change_values:
            change_error_keys.append(change_key)
        change_errors, change_fields = keys_missing(change_error_keys,
                                                    change_values)
        if len(change_errors) > 0:
            write_error_to_response(self.response,
                                    change_errors,
                                    missing_invalid_parameter)
            return

        # check invalidity
        invalid = key_validation(change_values)  # the change_values dictionary

        if len(invalid) > 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter)
            return

        user = User.get_by_id(int(values['userId']))
        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: "Listing not authorized"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        user_id = user.get_id()

        # make sure that the userId is the owner id of the listing
        listing_owner_id = listing.userId
        if listing_owner_id != user_id:
            error = {
                not_authorized[
                    'error']:
                        "Provided user ID does not match the owner id of " +
                        "the listing"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        assert(listing is not None)
        assert(len(invalid) == 0)
        assert(len(change_errors) == 0)
        assert valid
        assert (listing_owner_id == user_id)

        for key in change_values:
            if key != "isPublished":
                listing.set_property(key, change_values[key])
        # if isPublished field is changed from false to true,
        # check missing fields
        if is_existing_and_non_empty("isPublished", change_values):
            if (not listing.isPublished) and \
                    (convert_to_bool(change_values["isPublished"])):
                errors = fields_missing(listing)
                if len(errors) > 0:
                    write_error_to_response(self.response,
                                            errors,
                                            missing_invalid_parameter)
                    return
            listing.isPublished = convert_to_bool(change_values["isPublished"])

        listing.put()
        write_success_to_response(self.response, {
            'modifiedDate': str(datetime.datetime.now())})


def fields_missing(listing):
    """
    Checks if there are any fields that are None or empty in the listing.

    @param listing: the listing being checked
    @return: error messages if there's any empty fields. Otherwise, return empty dictionary
    """
    errors = {}
    assert listing is not None
    listing_keys_clone = copy.deepcopy(listing_keys)
    listing_keys_clone.remove("authToken")
    diffs = set(listing_keys_clone) - set(listing.__dict__['_values'].keys())
    if diffs != 0:
        for diff in diffs:
            error = missing[diff]['error']
            errors[error] = str(diff) + " is Missing"
        if not listing.__dict__['_values']['images']:
            image_error = missing['images']['error']
            errors[image_error] = "images is Missing"

    return errors
