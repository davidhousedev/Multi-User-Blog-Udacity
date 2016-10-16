""" Google Datastore Database Model for a Blog Post Comment

    Properties:
        content: Comment content (str)
        author: Comment author (str)
        created: Date and time when comment was posted (DateTime)

    Class Methods:
        get_comments(parent) - Gets all comments for a specific blog post

    Methods:
        render() - Replaces newlines with <br> in comment content,
        and stores in variable self._render_text
"""

import webapp2

from google.appengine.ext import db

class Comment(db.Model):
    """ Database model for a user """
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_comments(cls, parent):
        """ Returns an array of Comment entities
        for a parent Blog post """
        comment_arry = []
        comments = cls.all().ancestor(parent) # get all commentts for a post
        comments.order("-created") # order from most to least recent

        for comment in comments:
            comment.render() # replace newlines with <br>
            comment_arry.append(comment)

        return comment_arry

    def render(self):
        """ Replaces newlines in post content with <br>
        and saves to self._render_text"""
        self._render_text = self.content.replace('\n', '<br>')
