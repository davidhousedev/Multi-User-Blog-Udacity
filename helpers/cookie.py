""" Handles the creation and validation of user authentication cookies

Examples:


"""
import hmac
#from helpers.cookie_secret import secret as sec

# Source: Methods in this file were borrowed from Intro to Backend course material

#TODO: Change make(val) to accept secret from separate file

def make(val):
    """ Creates and returns valid cookie with HMAC encryption and server-secret """
    return str("%s|%s" % (val, hmac.new("CHANGEME", str(val)).hexdigest()))

def validate(cookie_val):
    """ Returns cookie_value, without hash, if valid. Otherwise, returns None """
    val = cookie_val.split("|")[0]
    if cookie_val == make(val):
        return val