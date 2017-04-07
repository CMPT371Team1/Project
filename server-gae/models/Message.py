import datetime
from google.appengine.ext import ndb


class Message(ndb.Model):
    """This Message class contains the fields associated with a message."""
    messageId = ndb.IntegerProperty(required=True, default=0)
    listingId = ndb.IntegerProperty(required=True)
    senderId = ndb.IntegerProperty(required=True)
    receiverId = ndb.IntegerProperty(required=True)
    message = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    received = ndb.BooleanProperty(required=True, default=False)
    createdDate = ndb.DateProperty(required=True,
                                   default=datetime.datetime.now())
