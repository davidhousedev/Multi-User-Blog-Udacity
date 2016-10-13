import webapp2

from google.appengine.ext import db

class Post(db.Model):
    """ Database model for a blog post """
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_edit = db.DateTimeProperty(auto_now=True)
    #TODO: Add author as property

    @classmethod
    def view_posts(cls, num=None):
        """ Returns a List of num (optional) most
        recent blog posts for all authors """
        post_list = []
        posts = Post.all().order("-created")

        for post in posts.run(limit=num):
            post_list.append(post)

        return post_list
view_posts()
    def render(self):
        """ Return a post's content,
        replacing new-line with <br> for HTML"""
        return self.content.replace('\n', '<br>')
