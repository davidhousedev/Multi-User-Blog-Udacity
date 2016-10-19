""" Handles hashing and verification of user passwords

Examples:
    make("some_username")
        * Returns a secure cookie of the format:
        "some_username|hmac_encrypted_username"

    validate("secure_cookie")
        * Returns the username in the secure cookie, if the cookie is valid.
        Otherwise, returns None.


"""
import hmac
from cookie_secret import secret as sec

# Source: Methods in this file were borrowed from Intro to Backend course
# material


def make(val):
    """ Creates and returns valid cookie
    with HMAC encryption and server-secret """
    return str("%s|%s" % (val, hmac.new(sec(), str(val)).hexdigest()))


def validate(cookie_val):
    """ Returns cookie_value, without hash, if valid.
    Otherwise, returns None """
    val = cookie_val.split("|")[0]
    if cookie_val == make(val):
        return val
