from extras.Utils import *
from models.Listing import Listing
from models.User import User
import sys
from API_NAME import contact_seller_api
from extras.Required_Fields import check_required_valid
from models.Message import Message
from extras.Check_Invalid import *
sys.path.append("../")
from extras.Base_Handler import BaseHandler


class ContactSeller(BaseHandler):
    """
    Post:
        @pre-cond: Expecting keys to be senderId, listingId, message, phone,
                   email, phone, email, received, createdDate, authToken
                   At least one of email or phone should be present.
                   Sender should have valid authToken.
        @post-cond: On success, A message is sent to owner of the listing.
        @return:   A new token if success with code 200, otherwise,
                    an appropriate error message and code.


    """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(contact_seller_api, self.request.POST,
                                 self.response)

        if not valid:
            return
        assert values['senderId'] is not None
        # find the correct sender with senderId
        sender = User.get_by_id(int(values['senderId']))

        if sender is None:
            error = {
                not_authorized['error']: 'Sender not authorized'
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return
        # check if the sender is a valid user
        valid_sender = sender.validate_token(int(values['senderId']), "auth", values['authToken'])
        if not valid_sender:
            write_error_to_response(self.response, {not_authorized['error']:
                                                    "not authorized to send messages"},
                                    not_authorized['status'])
            return

        assert valid_sender is not None
        assert sender is not None

        # find the correct listing with listingId
        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: "listingId not authorized"
            }
            write_error_to_response(self.response, error, un_auth_listing['status'])
            return

        # make sure the sender is not the owner of the listing
        if int(values['senderId']) == listing.userId:
            error = {
                unallowed_message_send['error']: "Can't send message to yourself"
            }
            write_error_to_response(self.response, error, unallowed_message_send['status'])
            return

        assert listing is not None

        # all set
        message = Message(senderId=int(values['senderId']),
                          listingId=int(values['listingId']),
                          message=values['message'],
                          phone=values['phone'],
                          email=values['email'],
                          receiverId = int(listing.userId)
                          )

        assert message is not None
        message.put()
        message.messageId = message.key.id()
        message.put()
        write_success_to_response(self.response, {})
