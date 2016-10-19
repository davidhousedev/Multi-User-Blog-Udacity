""" Renders home page, showing all blogs posted by all users

    Methods:
        get(self, msg=None) - Renders homepage with optional alert message

"""


import handler as handler
import models.post as db_post  # facilitates creation and query for blog posts
import models.comment as db_comment  # facilitates queries for comments


class MainPage(handler.Handler):

    """ Default HTTP Request Handler """

    def get(self, msg=None):
        """ Display 10 most recent blog posts """

        posts = db_post.Post.view_posts()

        # Get the number of comments for each post,
        # and store as int in each post.
        for post in posts:
            comment_arry = db_comment.Comment.get_comments(post)
            post.num_comments(len(comment_arry))

        if msg and self.user:
            if msg == "welcome":
                msg = "Welcome, %s" % self.user.username

        self.render("allblogs.html",
                    posts=posts,
                    user=self.user,
                    message=msg)
