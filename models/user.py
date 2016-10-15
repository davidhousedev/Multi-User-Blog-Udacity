import webapp2

from google.appengine.ext import db

class User(db.Model):
    """ Database model for a user """
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_key(cls, db_id):
        """ Returns a User object by param:id if found in database """
        key = db.Key.from_path("User", int(db_id))
        return db.get(key)

    @classmethod
    def by_name(cls, name):
        """ Returns a User object by param:name if found in database """
        key = db.Key.from_path("User", str(name))
        return db.get(key)

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
