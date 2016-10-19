""" Handles hashing and verification of user passwords

Examples:
    make("foobar", "baz123")
        * Use this method to create a hashed password to write to database
        * Returns hashed password for username: foobar and password baz123.


    validate("foobar", "baz123", "salt,hashed_pw")
        * Use this method to verify user"s login information.
        * Returns True if hash of username: foobar and password: baz123
        with salt from param[2] is equal to param[2]

"""
import random
import hashlib
from string import letters

# Source: Methods in this file were borrowed from Intro to Backend course
# materials


def make_salt(length=5):
    """ Returns a string of five random chars """
    return "".join(random.choice(letters) for x in xrange(length))


def make(username, password, salt=None):
    """ Returns a string formatted "salt|hashed_pw"
    An existing salt may be provided for verification purposes """
    if not salt:
        salt = make_salt()
    hashed_pw = hashlib.sha256(username + password + salt).hexdigest()
    return "%s,%s" % (salt, hashed_pw)


def validate(username, password, hashed_pw):
    """ Validates authenticity of user input username and password """
    salt = hashed_pw.split(",")[0]
    return hashed_pw == make(username, password, salt)
