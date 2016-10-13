import webapp2

from google.appengine.ext import db

# Class methods sourced from Intro to Backend course materials

class User(db.Model):
    """ Database model for a user """
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, id):
        """ Returns a User object by param:id if found in db """
        return User.get_by_id(id)

    @classmethod
    def by_name(cls, name):
        """ Returns a User object by param:name if found in db """
        return User.all().filter('name=', name).get()

    @classmethod
    def register(cls, username, pw_hash, email=None):
        """ Returns a User object """
        return User(username=username,
                    pw_hash=pw_hash,
                    email=email)
