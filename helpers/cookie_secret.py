""" Stores secret string used for HMAC encryption """

# NOTE: The secret in this file is not the same
#       as the secret used in production.
def secret():
    """ Returns secret phrase for HMAC encryption """
    return "turtles"
