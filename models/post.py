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
    def get_post(cls, user, post_id):
        """ Returns a Post object by param:user and param:id
        if found in database """
        key = db.Key.from_path("User", user, "Post", int(post_id))
        post = db.get(key)
        post.render()
        return post

    @classmethod
    def edit(cls, author, post_id, title=None, content=None):
        """ Edits title and/or content of specified post
        and writes changes to database """
        post = cls.get_post(author, post_id)
        if post:
            if title:
                post.title = title
            if content:
                post.content = content
            post.put()
            return True
        return False

    @classmethod
    def delete(cls, author, post_id):
        """ Deletes post at key path: author, post_id """
        db_key = db.Key.from_path("User", author, "Post", int(post_id))
        if db_key:
            db.delete(db_key)
            return True
        else:
            return False

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
    def like(cls, author, post_id, liker):
        """ If param:liker has not already liked Post:post_id,
        increase Post likes by 1, otherwise return false """
        post = cls.get_post(author, post_id)
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
