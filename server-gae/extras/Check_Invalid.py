from Utils import *


def key_validation(dictionary):
    """
    Checks the validity of a dictionary of keys.
    :precond dictionary is not null
    :param dictionary: Dictionary containing:  phone1, phone2, email,
    password, province, userId, listingId, price, bathrooms, bedrooms, sqft,
    isPublished, thumbnailImageIndex, liked, valuesRequired, maxLimit,
    listingIdList, lower, upper

    Everything not in the list is considered as valid
    :return: a dictionary containing all invalid keys.
    """
    assert dictionary is not None
    invalid = {}
    for key in dictionary:
        value = dictionary[key]
        if is_empty(value):
            continue
        if key in valid_check:
            if not valid_check[key](value):
                invalid[invalids[key]["error"]] = key + " is invalid"
    return invalid


def is_valid_integer(input_string):
    """
    Checks if input_string is an integer
    :precond input_string is not null
    :param input_string: A number or a string.
    :return: True if integer, otherwise false
    """

    assert input_string is not None
    try:
        input_string = int(input_string)
        return True
    except ValueError:
        return False


def is_valid_positive_integer(input_string):
    """
    Checks if input_string is a positive integer
    :precond input_string is not null
    :param input_string: A number or a string.
    :return: True if integer, otherwise false
    """

    assert input_string is not None
    try:
        input_string = int(input_string)
        if int(input_string) <= 0:
            raise ValueError
        return True
    except ValueError:
        return False


def is_valid_float(input_string):
    """
    Checks if input_string is a floating point number
    :precond input_string is not null
    :param input_string: A floating point number
    :return: True if float, otherwise false
    """
    assert input_string is not None
    try:
        float(input_string)
        return True
    except ValueError:
        return False


def is_valid_bathroom(input_string):
    """
    Checks if input_string is float or not
    :precond input_string is not null
    :param input_string: A number or a string.
    :return: True if float, otherwise false
    """
    assert input_string is not None
    try:
        br = float(input_string)
        if br < 0:
            raise ValueError
        if round(br) - br == 0 or round(br) - br == 0.5:
            return True
        else:
            return False
    except ValueError:
        return False


def is_valid_bool(input_string):
    """
    Checks if input_string is boolean or not
    :precond input_string is not null
    :param input_string: A number or a string.
    :return: True if boolean, otherwise false
    """
    assert input_string is not None
    input_string = str(input_string)

    if input_string in valid_true_booleans or input_string in valid_false_booleans:
        return True
    else:
        return False


def is_valid_json(json_str):
    """
    Checks if json_str is a valid json object or not.
    :precond: json_str is not None
    :param json_str: A json string.
    :return: True if a valid json string, otherwise false.
    """
    assert json_str is not None
    try:
        json.loads(json_str)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_phone(phone):
    """
    Checks if phone is valid phone or not. Valid here means, if it is of 10
    digits or not.
    :precond phone is not None
    :param phone: A number or a string.
    :return: True if a valid phone number, otherwise false
    """
    assert phone is not None
    phone = str(phone)
    return len(phone) == 10 and is_valid_integer(phone)


def is_valid_password(password):
    """
    Checks if password is a valid password or not. Valid passwords are >=8,
    and have at least one lower-case, upper-case, and numeric character.
    :precond password is not null
    :param password: String to be checked
    :return: true if password is valid, otherwise false
    """
    assert password is not None
    password = str(password)
    return len(password) >= 8 and any(s.islower() for s in password) \
           and any(s.isupper() for s in password) \
           and any(s.isdigit() for s in password)


def is_valid_string_listing(listing):
    """
    Checks if all the key in listing dictionary are contained in listing_keys
    :precond listing is not null
    :param listing: a listing dictionary
    :return: true if listing dictionary has all valid keys, otherwise false
    """
    assert listing is not None
    listing = str(listing)
    if len(listing) == 0:
        return True
    list_object = json.loads(listing)
    return not any(key not in listing_keys
                   for key in list_object)


def is_valid_integer_list(any_list):
    """
    Check if the complete list has all the integers or not.
    :param any_list: A list of items - strings or integers or other types.
    :return: true if all integers, otherwise false
    """
    list_object = json.loads(any_list)
    return not any(not is_valid_integer(str(listing_id)) for listing_id in
                   list_object)


def is_valid_email(email):
    """
    Checks if email is valid or not
    :precond email is not null
    :param email: email that is needed to tested
    :return: True if email is valid
    """
    assert email is not None
    return validate_email(str(email))


def is_valid_province(province):
    """
    Checks the validity of a province string
    :precond province is not null
    :param province: string that needs to be tested
    :return: true if valid province
    """
    assert province is not None
    return province.lower() in province_complete or \
           province.upper() in province_abbr


def is_valid_xor(dictionary, key1, key2):
    """
    Ensures both of the given keys are not in the dictionary.
    :param dictionary:
    :param key1: a key
    :param key2: another key
    :return: true if a valid xor
    """
    if key1 in dictionary and key2 in dictionary:
        return False
    else:
        return True


def is_valid_latitude(latitude):
    """
        Checks the validity of a latitude
        :precond latitude is not null
        :param latitude: string that needs to be tested
        :return: true if valid latitude
    """
    assert latitude is not None

    try:
        if is_valid_float(latitude):
            return MIN_LATITUDE <= float(latitude) <= MAX_LATITUDE
        else:
            return False
            # return -90 <= latitude and latitude <= 90
    except ValueError:
        return False


def is_valid_postal_code(postal_code):
    """
        Checks the validity of a Canadian postal code string
        :precond postal_code is not null
        :param postal_code: string that needs to be tested
        :return: true if valid Canadian postal code
        N.B. Postal code must be a canadian postal code.
        N.B. To check this, postal_code must be in the form A1A1A1 with no spaces in between characters.
    """
    assert postal_code is not None
    postal_code = postal_code.replace(" ", "")
    postal_code_re = re.compile(r"\s*(\w\d\s*){3}\s*")
    return postal_code_re.match(postal_code) is not None


def is_valid_longitude(longitude):
    """
        Checks the validity of a longitude
        :precond longitude is not null
        :param longitude: float that needs to be tested
        :return: true if valid longitude
        """
    assert longitude is not None
    try:
        if is_valid_float(longitude):
            return MIN_LONGITUDE <= float(longitude) <= MAX_LONGITUDE
        else:
            return False
            # return -180 <= longitude and longitude <= 180
    except ValueError:
        return False


def is_valid_images(images):
    try:
        json.loads(images)
    except ValueError:
        return False
    return True


valid_check = {
    "phone1": is_valid_phone,
    "phone2": is_valid_phone,
    "email": is_valid_email,
    "password": is_valid_password,
    "province": is_valid_province,
    "userId": is_valid_integer,
    "listingId": is_valid_integer,
    "price": is_valid_positive_integer,
    "bathrooms": is_valid_bathroom,
    "bedrooms": is_valid_positive_integer,
    "squareFeet": is_valid_positive_integer,
    "isPublished": is_valid_bool,
    "thumbnailImageIndex": is_valid_integer,
    "liked": is_valid_bool,
    "valuesRequired": is_valid_string_listing,
    "maxLimit": is_valid_integer,
    "listingIdList": is_valid_integer_list,
    "lower": is_valid_integer,
    "upper": is_valid_integer,
    "images": is_valid_images,
    "latitude": is_valid_latitude,
    "longitude": is_valid_longitude,
    "postalCode": is_valid_postal_code,
    "messageId": is_valid_integer,
    "readDel": is_valid_read_del,
    "fbId": is_valid_integer,
    "senderId": is_valid_integer,
    "receiverId": is_valid_integer,
    "changeValues": is_valid_json
}

