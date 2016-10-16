""" Google Datastore Database Model for a User

    Properties:
        username - This user's username (str)
        pw_hash - Hashed version of user's password (str)
        email - User's email, if provided (str)
        created - Date and time of user's creation (DateTime)

    Class Methods:
        by_username(username) - Returns a User entity by username
        register(username, pw_hash, email=None) - Creates a new user
"""

import webapp2

from google.appengine.ext import db

class User(db.Model):
    """ Database model for a user """
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_username(cls, username):
        """ Returns a User object by param:username if found in database """
        key = db.Key.from_path("User", str(username)) # generates key path to specific user
        return db.get(key) # returns db entity corresponding to key

    # Source: Intro to Backend course materials
    @classmethod
    def register(cls, username, pw_hash, email=None):
        """ Creates user object and writes to database """
        user = User(key_name=username,
                    username=username,
                    pw_hash=pw_hash,
                    email=email)
        user.put()
        return user
