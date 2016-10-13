import webapp2

from google.appengine.ext import db

class Post(db.Model):
    """ Database model for a blog post """
    title = db.StringPropert(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_edit = db.DateTimeProperty(auto_now=True)

    def render(self):
        """ Return a post's content,
        replacing new-line with <br> for HTML"""
        return self.content.replace('\n', '<br>')