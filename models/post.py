""" Google Datastore Database Model for a Blog Post

    Properties:
        author: Blog post author (str)
        title: Blog post title (str)
        content: Blog post content (str)
        likes: Blog's number of likes (int)
        users_liked: List of users who have liked the blog (list)
        created: Date and time when comment was posted (DateTime)
        last_edit: Date and time of most recent edit (DateTime)
        _render_text: Content of blog with newlines replaced by <br>s (str)
        _num_comments: Current number of comments for a specific blog post (str)

    Class Methods:
        get_post(author, post_id) - Returns a single post by author and post_id
        edit(author, post_id, title=None, content=None) - Edits either title or content of blog post
        delete(author, post_id) - Deletes a blog post from the database
        view_posts(num=None, parent=None) - Returns all posts from a specific user
        like(author, post_id, liker) - Likes or unlikes a post

    Methods:
        render() - Replaces newlines with <br> in comment content,
        and stores in variable self._render_text
        num_comments(num) - Updates post's number of comments to num
"""

import webapp2

from google.appengine.ext import db


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
    def get_post(cls, author, post_id):
        """ Returns a Post object by param:author and param:id
        if found in database """
        key = db.Key.from_path("User", author,
                               "Post", int(post_id))  # establish a db key
        post = db.get(key)  # use that key to retrieve a db entity
        post.render()  # replace newlines with <br>
        return post

    @classmethod
    def edit(cls, author, post_id, title=None, content=None):
        """ Edits title and/or content of specified post
        and writes changes to database """
        post = cls.get_post(author, post_id)
        if post:
            if title:
                post.title = title  # edit title if changed
            if content:
                post.content = content  # edit content if changed
            post.put()
            return True
        return False

    @classmethod
    def delete(cls, author, post_id):
        """ Deletes post at key path: author, post_id """
        db_key = db.Key.from_path("User", author, "Post", int(post_id))
        if db_key:
            db.delete(db_key)  # delete the entity matching db_key
            return True
        else:
            return False

    @classmethod
    def view_posts(cls, num=None, parent=None):
        """ Returns a List of num (optional) most
        recent blog posts for all authors """
        post_list = []
        posts = cls.all()  # query db for all Posts
        if parent:
            posts.ancestor(parent)  # filter query by author
        posts.order("-created")  # order posts, most recent first

        for post in posts.run(limit=num):
            post.render()  # replace newlines with <br>
            post_list.append(post)
        return post_list

    @classmethod
    def like(cls, author, post_id, liker):
        """ Either like, or unlike, a post depending on
        whether or not param:liker has already liked the post """
        post = cls.get_post(author, post_id)
        # if has this user already liked this post
        if liker in post.users_liked:
            post.users_liked.remove(str(liker))
            post.likes -= 1
        else:
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
