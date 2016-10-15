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
        comments = Comment.all().ancestor(parent)
        comments.order("-created")

        for comment in comments:
            comment.render()
            comment_arry.apppend(comment)

        return comment_arry

    def render(self):
        """ Replaces newlines in post content with <br>
        and saves to self._render_text"""
        self._render_text = self.content.replace('\n', '<br>')
