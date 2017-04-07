import random
import string
import json
import webapp2


def get_random_string(n=random.randint(10, 20), lower_case=0, upper_case=0,
                      numbers=0):
    """
    Creates a random string with the given properties
    :param n: length of the string
    :param lower_case: LEAST number of lower case characters
    :param upper_case: LEAST number of upper case characters
    :param numbers: LEAST number of numeric characters
    :return: a random string of length n
             with at least lower_case number of  lower case characters,
                  at least upper_case number of upper case characters,
                  at least numbers number of numerical digits.
    N.B. The string only returns an alpha-numeric string, without any special characters.
    """
    s = ""
    if lower_case == upper_case == numbers == 0:
        s = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase) for
                    _
                    in range(n))
    else:
        new_n = n - lower_case - upper_case - numbers
        if new_n > 0:
            s = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits + string.ascii_lowercase)
                        for _
                        in range(new_n))
        s += ''.join(random.SystemRandom().choice(string.ascii_lowercase)
                     for _
                     in range(lower_case))
        s += ''.join(random.SystemRandom().choice(string.ascii_uppercase)
                     for _
                     in range(upper_case))
        s += ''.join(random.SystemRandom().choice(string.digits)
                     for _
                     in range(numbers))

    return s


def get_random_email():
    """
    Return the random valid email, in format <a>@<b>.ca
     where <a> is of length in between 6 and 12
           <b> is of length in between 4 and 12
    :return: a string representing email
    """

    return get_random_string(random.randint(6, 12)) + "@" + \
           get_random_string(random.randint(4, 6)) + ".ca"


def get_random_password():
    """
    a random password with all alpha-numeric digits
    :return: a string containing a random password
      where the password is of length between 8 to 16 characters
      with one uppercase, one lowercase and one numerical digit.
    """

    return get_random_string(random.randint(8, 16), 1, 1, 1)


def get_random_postal_code():
    """
    Returns a random postalCode
    :return: a string containing a random password
    """
    postal_code = ''
    for i in range(0, 3):
        # In one iteration, produce a capital letter and a digit.
        postal_code += (
        get_random_string(1, 0, 1, 0) + str(random.randint(0, 9)))
    return postal_code


def create_dummy_users_for_testing(main, n):
    """
     Creates n dummy users with random values.
    :param main: Main handler, to make an api call.
    :param n: number of dummy users required.
    :return: a dictionary containing: email, first name,
     last name, city, postalCode, phone number1, phone number2 (optionally)
     "SK" as a province, userId, and a token as keys.
    """
    users = []
    n_copy = n
    assert n > 0
    while n > 0:
        password = get_random_password()
        new_user = {"email": get_random_email(),
                    "password": password,
                    "firstName": get_random_string(),
                    "lastName": get_random_string(),
                    "city": get_random_string(),
                    "province": "SK",
                    "phone1": get_random_string(10, numbers=10),
                    "phone2": get_random_string(10, numbers=10)
                    if random.randint(0, 1) else "",
                    "confirmedPassword": password
                    }
        request = webapp2.Request.blank('/createUser', POST=new_user)
        response = request.get_response(main.app)
        output = json.loads(response.body)
        del new_user["confirmedPassword"]
        new_user["authToken"] = str(output["authToken"])
        new_user["userId"] = str(output["userId"])
        users.append(new_user)
        n -= 1
    assert len(users) == n_copy
    return users


def create_dummy_listings_for_testing(main, num_listings, num_users=1):
    """
    Creates "num_listings" dummy users and listings. All of the fields will be randomized,
    with the exception of Province, which will be SK (Saskatchewan)

    :param main: Main handler
    :param num_listings: number of dummy listings to create
    :param num_users: number of users to assign listings to
    :return: a dictionary of listing with all listing data as keys and listingID
    """
    listings = []
    assert num_listings >= num_users
    assert num_users != 0

    users = create_dummy_users_for_testing(main, num_users)
    assert len(users) == num_users
    for i in range(0, num_users):
        if i == num_users - 1 and num_listings % num_users != 0:
            distribution = num_listings // num_users + 1
        else:
            distribution = num_listings // num_users
        user = users[i]
        for j in range(0, distribution):
            random_listing_info = {"userId": user["userId"],
                                   "authToken": user["authToken"],
                                   "bedrooms": str(random.randint(1, 10)),
                                   "longitude": str(random.randint(-180, 180)),
                                   "latitude": str(random.randint(-90, 90)),
                                   "postalCode": get_random_postal_code(),
                                   "squareFeet": str(random.randint(50, 12000)),
                                   "bathrooms": str(random.randint(1, 10)),
                                   "price": str(
                                       random.randint(100000, 2000000)),
                                   "description": " ".join(
                                       [get_random_string() for _ in
                                        range(random.randint(15, 45))]) + ".",
                                   "isPublished": str(
                                       bool(random.randint(0, 1))),
                                   "province": "SK",
                                   "city": get_random_string(),
                                   "address": get_random_string(),
                                   "thumbnailImageIndex": 0,
                                   "images": json.dumps(['some images',
                                                         'some images 2'])
                                   }

            request = webapp2.Request.blank('/createListing',
                                            POST=random_listing_info)
            response = request.get_response(main.app)
            output = json.loads(response.body)
            random_listing_info["listingId"] = output["listingId"]
            listings.append(random_listing_info)

    return listings, users


def create_random_user():
    """
    :return: a randomly generated user profile
    """
    password = get_random_password()
    user = {"email": get_random_email(),
            "password": password,
            "firstName": get_random_string(),
            "lastName": get_random_string(),
            "city": get_random_string(),
            "province": "SK",
            "phone1": get_random_string(10, numbers=10),
            "phone2": get_random_string(10, numbers=10)
            if random.randint(0, 1) else "", "confirmedPassword": password}
    return user


def create_random_listing(user_id, token):
    """
    Creates a ranom listing attached to the user_id and the token
    :param user_id: User Id where listing belongs
    :param token: the authorization token of the new random listing
    :return: a listing with randomly generated fields
    """
    random_listing = {"userId": user_id,
                      "authToken": token,
                      "bedrooms": str(random.randint(1, 10)),
                      "longitude": str(random.randint(-180, 180)),
                      "latitude": str(random.randint(-90, 90)),
                      "postalCode": get_random_postal_code(),
                      "squareFeet": str(random.randint(50, 12000)),
                      "bathrooms": str(random.randint(1, 10)),
                      "price": str(random.randint(100000, 2000000)),
                      "description": " ".join(
                          [get_random_string() for _ in
                           range(random.randint(15, 45))]) + ".",
                      "isPublished": str(bool(random.randint(0, 1))),
                      "province": "SK",
                      "city": get_random_string(),
                      "address": get_random_string(),
                      "thumbnailImageIndex": 0,
                      "images": json.dumps(['some images', 'some images 2'])
                      }
    return random_listing
