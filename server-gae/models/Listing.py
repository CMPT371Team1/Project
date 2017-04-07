import json
import sys
from google.appengine.ext import ndb
sys.path.append("../")

DEFAULT_BEDROOMS_MAX = 10
DEFAULT_BEDROOMS_MIN = 1
DEFAULT_BATHROOMS_MAX = 10.0
DEFAULT_BATHROOMS_MIN = 1.0
DEFAULT_SQFT_MAX = 10000
DEFAULT_SQFT_MIN = 0
DEFAULT_PRICE_MAX = 999999999
DEFAULT_PRICE_MIN = 10


class Listing(ndb.Model):
    """This Listing class contains the functions
    and fields associated with a listing."""
    bedrooms = ndb.IntegerProperty(required=False)
    squareFeet = ndb.IntegerProperty(required=False)
    bathrooms = ndb.FloatProperty(required=False)
    price = ndb.IntegerProperty(required=False)
    description = ndb.StringProperty(required=False)
    isPublished = ndb.BooleanProperty(required=True)
    province = ndb.StringProperty(required=False)
    city = ndb.StringProperty(required=False)
    images = ndb.BlobProperty(required=False, repeated=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=False)
    userId = ndb.IntegerProperty(required=True)
    address = ndb.StringProperty(required=False)
    listingId = ndb.IntegerProperty(required=False)
    longitude = ndb.FloatProperty(required=False)
    latitude = ndb.FloatProperty(required=False)
    postalCode = ndb.StringProperty(required=False)

    """
    Assign the default values for min and max of bedrooms, bathrooms, sqFt, and price
    """
    numeric_filter_bounds = {
        "bedrooms_min": DEFAULT_BEDROOMS_MIN,
        "bedrooms_max": DEFAULT_BEDROOMS_MAX,
        "bathrooms_min": DEFAULT_BATHROOMS_MIN,
        "bathrooms_max": DEFAULT_BATHROOMS_MAX,
        "sqft_min": DEFAULT_SQFT_MIN,
        "sqft_max": DEFAULT_SQFT_MAX,
        "price_min": DEFAULT_PRICE_MIN,
        "price_max": DEFAULT_PRICE_MAX
    }

    @classmethod
    def reset_filter(cls):
        """
        Resets the filter to the default max and min values
        :return: Nothing
        """
        cls.numeric_filter_bounds['bedrooms_min'] = DEFAULT_BEDROOMS_MIN
        cls.numeric_filter_bounds['bedrooms_max'] = DEFAULT_BEDROOMS_MAX
        cls.numeric_filter_bounds['bathrooms_min'] = DEFAULT_BATHROOMS_MIN
        cls.numeric_filter_bounds['bathrooms_max'] = DEFAULT_BATHROOMS_MAX
        cls.numeric_filter_bounds['sqft_min'] = DEFAULT_SQFT_MIN
        cls.numeric_filter_bounds['sqft_max'] = DEFAULT_SQFT_MAX
        cls.numeric_filter_bounds['price_min'] = DEFAULT_PRICE_MIN
        cls.numeric_filter_bounds['price_max'] = DEFAULT_PRICE_MAX

    def set_bedrooms(self, bedrooms):
        """
        Setter for the field bedrooms
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.bedrooms = int(bedrooms)

    def set_bathrooms(self, bathrooms):
        """
        Setter for the field bathrooms
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.bathrooms = float(bathrooms)

    def set_price(self, price):
        """
        Setter for the field price
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.price = int(price)

    def set_description(self, description):
        """
        Setter for the field description
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.description = description

    def set_is_published(self, is_published):
        """
        Setter for the field isPublished
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.isPublished = is_published == 'True'

    def set_province(self, province):
        """
        Setter for the field province
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.province = province

    def set_city(self, city):
        """
        Setter for the field city
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.city = city

    def set_images(self, images):
        """
        Setter for the field images
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.images = images

    def set_thumbnail_index(self, index):
        """
        Setter for the field thumbnailIndex
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.thumbnailImageIndex = int(index)

    def set_address(self, address):
        """
        Setter for the field address
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.address = address

    def set_listing_id(self, listing_id):
        """
        Setter for the field listingId
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.listingId = listing_id

    def set_squareFeet(self, squareFeet):
        """
        Setter for the field squareFeet
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.squareFeet = int(squareFeet)

    def set_longitude(self, longitude):
        """
        Setter for the field longitude
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.longitude = float(longitude)

    def set_latitude(self, latitude):
        """
        Setter for the field latitude
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.latitude = float(latitude)

    def set_postalCode(self, postal_code):
        """
        Setter for the field postalCode
        :param: bedrooms: value for the field
        :return: Nothing
        """
        self.postalCode = postal_code

    def set_property(self, key, value):
        """
        Setter for corresponding field according to key name
        :param key: the field name
        :param value: the value to put in that field
        :return: Nothing
        """
        _key_to_set = {
            "price": self.set_price,
            "squareFeet": self.set_squareFeet,
            "bathrooms": self.set_bathrooms,
            "bedrooms": self.set_bedrooms,
            "description": self.set_description,
            "province": self.set_province,
            "isPublished": self.set_is_published,
            "address": self.set_address,
            "thumbnailImageIndex": self.set_thumbnail_index,
            "images": self.set_images,
            "listingId": self.set_listing_id,
            "city": self.set_city,
            "longitude": self.set_longitude,
            "latitude": self.set_latitude,
            "postalCode": self.set_postalCode
        }
        _key_to_set[key](value)

    def get_value_from_key(self, key):
        """
        Getter for corresponding value according to key name
        :param key: the field name
        :return: the value in that field
        """
        assert key is not None
        assert key != ""
        _key_to_get_value = {
            "price": self.price,
            "city": self.city,
            "squareFeet": self.squareFeet,
            "bathrooms": self.bathrooms,
            "bedrooms": self.bedrooms,
            "description": self.description,
            "province": self.province,
            "isPublished": self.isPublished,
            "address": self.address,
            "userId": self.userId,
            "thumbnailImageIndex": self.thumbnailImageIndex,
            "images": self.images,
            "listingId": self.listingId,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "postalCode": self.latitude
        }
        return _key_to_get_value[key]

    @classmethod
    def get_key(cls, key):
        """
        Returns the desired key from the class.
        :precond key is not null
        :param key: A string representing the desired key in the class.
        :return:  The key from the class
        N.B. Python doesn't have switch cases.
        """
        assert key is not None
        assert key != ''
        return cls.get_value_from_key(cls, key)


