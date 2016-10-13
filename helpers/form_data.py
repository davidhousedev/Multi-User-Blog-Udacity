import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def username(username):
    """ Returns param:username if valid """
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def password(password):
    """ Returns param:password if valid """
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def email(email):
    """ Returns param:email if valid """
    #TODO: double check syntax
    return not email or EMAIL_RE.match(email)