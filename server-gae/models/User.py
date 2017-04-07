import time
import webapp2_extras
from google.appengine.ext import ndb
from webapp2_extras import security
from webapp2_extras.appengine.auth.models import User as Webapp2User


class User(Webapp2User):
    '''This User class contains the functions
    and fields associated with a User.'''

    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=False)
    phone1 = ndb.StringProperty(required=False)
    phone2 = ndb.StringProperty(required=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=False)

    def set_password(self, raw_password):
        """Sets the password for the current user
        :param raw_password:
            The raw password which will be hashed and stored
        """
        self.password = security.generate_password_hash(raw_password)
        self.put()

    # @classmethod
    # def build_key(cls, email):
    #     return ndb.Key(cls, email)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """
        Returns a Monad tuple of user object based on a user ID and token
        :param user_id: The user_id of the requesting user
        :param token: The token string to be verified
        :param subject: the subject - default is "auth"
        :returns A monad tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
        """

        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)

        # Use get_multi() to save a RPC call
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

    def set_phone1(self, phone1):
        self.phone1 = phone1

    def set_phone2(self, phone2):
        self.phone2 = phone2

    def set_email(self, email):
        if self.email in self.auth_ids:
            self.auth_ids.remove(self.email)
        self.email = email
        self.add_auth_id(self.email)
        self.verified = False

    def set_province(self, province):
        self.province = province

    def set_city(self, city):
        self.city = city

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    _key_to_set_value = {
        "email": set_email,
        "firstName": set_first_name,
        "lastName": set_last_name,
        "phone1":set_phone1,
        "phone2":set_phone2,
        "province": set_province,
        "city": set_city
    }

    def set_property(self, key, value):
        self._key_to_set_value[key](self, str(value))

    _optional = ["phone2"]
    _required_fields = ["email", "firstName", "lastName", "phone1",
                        "phone2", "province", "city"]

    def get_from_key(self, key):
        _key_to_get_value = {
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "phone1": self.phone1,
            "phone2": self.phone2,
            "province": self.province,
            "city": self.city
        }
        assert key in _key_to_get_value
        return _key_to_get_value[key]

    def __cmp__(self, other):
        """
        Compares if two users have same data
        :param other: Other user
        :return:
        """
        if type(other) != type(self):
            return False
        for key in self._required_fields:
            if self.get_from_key(key) != other.get_from_key(key):
                return False
        return True

    def compare_with_dictionary(self, dictionary):
        """
        Checks if this object has same values as the user in dictionary.
        :param dictionary: a user dictionary
        :return: True if object has equal values as the dictionary
        """
        for key in self._required_fields:
            if key in dictionary:
                if self.get_from_key(key) != dictionary[key]:
                    return False
            elif key not in self._optional:
                return False
        return True
