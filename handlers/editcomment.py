""" Renders comment editing form and handles deleting comment in db """

import handler as handler
import models.comment as db_comment
import models.post as db_post

class EditComment(handler.Handler):
    """ Handler for editing comments """
    def get(self, author, post_id, comment_id):
        post = db_post.Post.get_post(author, post_id)
        comment = db_comment.Comment.get_by_id(author,
                                               post_id,
                                               comment_id)
        if self.user.username != comment.author:  # did user write comment?
            return self.redirect("/post" "/%s/%s" % (author, post_id))
        self.render("editcomment.html",
                    post=post,
                    comment=comment)