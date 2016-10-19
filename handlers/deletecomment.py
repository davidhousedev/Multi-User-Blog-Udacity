""" Deletes comment from database """

import handler as handler
import models.comment as db_comment


class DeleteComment(handler.Handler):

    """ Queries database for specified comment and deletes if found """

    def post(self, author, post_id, comment_id):
        """ Receives submission from delete button to delete a comment """
        if self.user.username == author:
            db_comment.Comment.delete(author,
                                      post_id,
                                      comment_id)
        self.redirect("/post" "/%s/%s" % (author, post_id))
