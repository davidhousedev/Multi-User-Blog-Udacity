""" Displays a single post, and facilitates post comment creation

    get(self, user, post_id) - Renders a specific post and its comments
    post(self, user, post_id) - Writes a user's comment to databse

"""

import handler as handler
import models.post as db_post # facilitates creation and query for blog posts
import models.comment as db_comment # facilitates queries for comments

class ViewPost(handler.Handler):
    """ Renders a single blog post via a permalink """
    def get(self, user, post_id):
        """ Displays a single post """
        if not post_id and user:
            self.redirect("/")
            return

        post = db_post.Post.get_post(user, post_id)
        comments = db_comment.Comment.get_comments(post)
        self.render("viewpost.html",
                    post=post,
                    comments=comments,
                    user=self.user)

    def post(self, user, post_id):
        """ Records posted comment to database """
        if self.user:
            content = self.request.get("content")
            if not content:
                self.redirect("/%s/%s" % (user, post_id))
            parent_post = db_post.Post.get_post(user, post_id)
            comment = db_comment.Comment(parent=parent_post,
                                         content=content,
                                         author=self.user.username)
        comment.put()
        self.redirect("/post" "/%s/%s" % (user, post_id))