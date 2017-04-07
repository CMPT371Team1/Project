from Error_Code import *
from API_NAME import *
import Utils
from extras.Check_Invalid import *
from models.User import User

"""
   Dictionary with all fields that are required per API call
"""

required_api_dict = {
    sign_in_api: ['email', 'password'],
    create_user_api: ['email', 'firstName', 'password', 'confirmedPassword',
                      'phone1', 'province', 'city'],
    change_password_api: ['oldPassword', 'newPassword', 'confirmedPassword',
                          'userId'],
    contact_seller_api: ['senderId', 'listingId', 'message', 'phone',
                         'email', 'authToken', 'receiverId'],
    create_listing_api: ["isPublished", "userId", "authToken"],
    delete_listing_api: ['userId', 'listingId', 'authToken'],
    edit_listing_api: ['changeValues', 'userId', 'listingId', 'authToken'],
    edit_message_api: ['messageId', 'userId', 'authToken', 'readDel'],
    edit_user_api: ['changeValues', 'userId', 'authToken'],
    fb_login_api: ['fbId'],
    get_favourites_listing_api: ['userId', 'authToken'],
    get_listing_api: [],
    get_messages_api: ['userId', 'authToken'],
    get_my_listings_api: ['userId', 'authToken'],
    like_listing_api: ['userId', 'listingId', 'liked', 'authToken'],
    sign_in_token_api: ['authToken', 'userId'],
    sign_out_api: ['userId', 'authToken']
}


def check_required_valid(api, post, response, auth_required=False):
    """
    Method check if the response post request does not have any missing fields,
    and also check if all the present fields are valid or not. If auth_required
    is true then post request is made sure to have a valid user, which has valid
    userId and authToken.
    If every field is present and user is authenticated (if required) then
    dictionary of all values present in the post request is converted to python
    dictionary.

    :param api: api name to which post request is being made
    :param post: post request that was sent by the user
    :param response: response object on which error needs to be written
    if required
    :param auth_required: if user authentication is required in the post request
    :return: A tuple of (bool, dictionary) is returned where bool represents if
    fields are valid and dictionary is the converted values dictionary.
    If post request has  missing fields, invalid fields or unauthenticated user
    then (False, None) is returned otherwise (True, values) is returned.
    """

    # validating if request has all required key
    errors, values = Utils.keys_missing(required_api_dict[api], post)

    # if any of the keys is missing then error is written to the response
    if len(errors) > 0:
        Utils.write_error_to_response(response, errors,
                                      missing_invalid_parameter)
        return False, None

    invalid = key_validation(values)

    # if any of the keys is invalid then error is written to the response
    if len(invalid) > 0:
        Utils.write_error_to_response(response, invalid,
                                      missing_invalid_parameter)
        return False, None

    assert len(errors) == 0
    assert len(invalid) == 0

    if auth_required:
        # checking if the user with userId provided exists in DB
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            Utils.write_error_to_response(response, error,
                                          not_authorized["status"])
            return False, None

        # checking if the user has provided valid token
        valid_user = user.validate_token(int(values["userId"]),
                                         "auth", values["authToken"])

        if not valid_user:
            Utils.write_error_to_response \
                (response,
                 {not_authorized['error']: "not authorized"},
                 not_authorized['status'])
            return False, None

        assert valid_user
        assert user is not None

    assert len(errors) == 0
    assert len(invalid) == 0

    return True, values
