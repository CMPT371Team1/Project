from google.appengine.ext import ndb


class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    listingId = ndb.IntegerProperty(required=True, default=0)
    userId = ndb.IntegerProperty(required=True)
    bedrooms = ndb.IntegerProperty(required=True)
    sqft = ndb.IntegerProperty(required=True)
    bathrooms = ndb.IntegerProperty(required=True)
    price = ndb.IntegerProperty(required=True)
    description = ndb.StringProperty(required=True)
    isPublished = ndb.BooleanProperty(required=True, default=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=True, default=0)
    images = ndb.BlobProperty()

