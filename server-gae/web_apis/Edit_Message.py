import sys
from extras.Utils import *
from extras.Check_Invalid import *
from models.Message import Message
from models.User import User
from API_NAME import edit_message_api
from extras.Required_Fields import check_required_valid

sys.path.append("../")


class EditMessage(webapp2.RequestHandler):
    """
    EditMessage class is used to respond to request to editMessage api.
    The post method in this class is used to edit the given message.
     Post:
         @pre-cond: Expecting keys to be userId, messageId, readDel and
                    authToken.
                    User with provided userId should be present in the database.
                    authToken should be valid for given userId.
                    message with messageId should be present in the database.
                    message should belong the user requesting to edit.
                    readDel should be either r, R, d, D which represents read
                    or delete.
         @post-cond: If readDel is r or R then message is set to read, otherwise
                     if it is d or D then message is deleted from the database.
         @return-api: Nothing is being returned in this API
     """
    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(edit_message_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        message = Message.get_by_id(int(values["messageId"]))

        if message is None:
            write_error_to_response(self.response, {
                invalid_message_id['error']:
                    "Message doesn't exist with this message id"},
                                    invalid_message_id['status'])
            return

        if message.receiverId != int(values['userId']):
            write_error_to_response(self.response, {
                not_authorized['error']: "not authorized to edit this message"},
                                    not_authorized['status'])
            return
        # r represent read
        if values["readDel"] in ["r", "R"]:
            message.received = True
            message.put()
        # d represent delete
        elif values["readDel"] in ["d", "D"]:
            message.key.delete()
        write_success_to_response(self.response, {})
