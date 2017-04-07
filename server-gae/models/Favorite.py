from google.appengine.ext import ndb


class Favorite(ndb.Model):
    """This Favorite class contains the fields associated with a favorite
     if user like/dislike a listing."""
    listingId = ndb.IntegerProperty(required=True)
    userId = ndb.IntegerProperty(required=True)
    liked = ndb.BooleanProperty(required=True, default=True)
