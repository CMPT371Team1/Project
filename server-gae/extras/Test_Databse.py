from extras.Random_Models import *


def get_user(name, email, password):
    user = create_random_user()
    user["firstName"] = name
    user["email"] = email
    user["password"] = password
    user["confirmedPassword"] = password
    return user


def get_listings(bedrooms, price, bathrooms, is_published, province,
                 square_feet):
    listing = create_random_listing("", "")
    listing["bedrooms"] = bedrooms
    listing["price"] = price
    listing["bathrooms"] = bathrooms
    listing["isPublished"] = is_published
    listing["province"] = province
    listing["squareFeet"] = square_feet
    return listing


users = [
    get_user("Tester 1", "test1@test.com", "123abcABC"),
    get_user("Tester 2", "test2@test.com", "123abcABC"),
    get_user("Tester 3", "test3@test.com", "123abcABC")
]

listings_published = [
    get_listings(10, 100000, 1.5, True, "SK", 10015220),
    get_listings(4, 1002000, 2.5, True, "AB", 10010510),
    get_listings(6, 9010000, 10, True, "SK", 40000231),
    get_listings(4, 1234213, 12, True, "AB", 100101320),
    get_listings(1, 5614132, 1, True, "SK", 400012340),
    get_listings(5, 23452641, 2, True, "AB", 100623100),
    get_listings(9, 2346163, 10, True, "SK", 123440000),
    get_listings(12, 1213515, 8, True, "AB", 100101230),
    get_listings(9, 62346234, 9, True, "SK", 4000033),
    get_listings(1, 123412, 5, True, "AB", 100100123),
    get_listings(22, 7534634, 40, True, "SK", 4000001234),
    get_listings(4, 120000, 5, True, "YT", 5000)
]

listing_unpublished = [
    get_listings(10, 100000, 3.5, False, "ON", 12110),
    get_listings(4, 1002000, 4.5, False, "ON", 111001),
    get_listings(6, 1000, 99, False, "AB", 101010)
]

random_listings = 100
random_users = 10
