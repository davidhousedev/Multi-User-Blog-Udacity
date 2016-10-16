""" Handles hashing and verification of user passwords

Examples:
    username("some_username")
    password("some_unencrypted_password")
    email("some_email")
        * Returns a Match object if valid, otherwise returns None

"""
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def username(username):
    """ Returns a Match object if valid """
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def password(password):
    """ Returns a Match object if valid """
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def email(email):
    """ Returns a Match object if valid """
    return not email or EMAIL_RE.match(email)