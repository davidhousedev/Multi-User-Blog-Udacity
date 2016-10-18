""" Queries Database for a specified post. If found, deletes that post """

import handler as handler
import models.post as db_post  # facilitates creation and query for blog posts

class DeletePost(handler.Handler):
    """ Queries database for a post and deletes it if found """
    def post(self, author, post_id):
        """ If current user is author, delete's Post:post_id.
        Otherwise, redirects back to post """
        if self.user.username == author:
            if db_post.Post.delete(author, post_id):
                self.redirect("/")
                return
        self.redirect("/post" "/%s/%s" % (author, post_id))