import webapp2

from google.appengine.ext import db
#TODO: Add 'likes'
#TODO: Add post edit capabilities
class Post(db.Model):
    """ Database model for a blog post """
    author = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    likes = db.IntegerProperty(required=True)
    users_liked = db.StringListProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_edit = db.DateTimeProperty(auto_now=True)

    @classmethod
    def get_post(cls, user, db_id):
        """ Returns a Post object by param:user and param:id
        if found in database """
        key = db.Key.from_path("User", user, "Post", int(db_id))
        post = db.get(key)
        post.render()
        return post

    @classmethod
    def view_posts(cls, num=None, parent=None):
        """ Returns a List of num (optional) most
        recent blog posts for all authors """
        post_list = []
        posts = Post.all()
        if parent:
            posts.ancestor(parent)
        posts.order("-created")

        for post in posts.run(limit=num):
            post.render()
            post_list.append(post)
        return post_list

    @classmethod
    def like(cls, author, db_id, liker):
        """ If param:liker has not already liked Post:db_id,
        increase Post likes by 1, otherwise return false """
        post = cls.get_post(author, db_id)
        if liker in post.users_liked:
            return False
        post.likes += 1
        post.users_liked.append(str(liker))
        post.put()
        return True

    def render(self):
        """ Replaces newlines in post content with <br>
        and saves to self._render_text"""
        self._render_text = self.content.replace('\n', '<br>')

    def num_comments(self, num):
        """ Stores the number (num) of comments as a property """
        self._num_comments = str(num)
