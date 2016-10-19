""" Facilitates liking and unliking of posts """

import handler as handler
import models.post as db_post  # facilitates creation and query for blog posts


class LikePost(handler.Handler):

    """ Increase or decrease post likes by 1 """

    def get(self, *args):
        post_author = args[0]
        post_id = args[1]
        user_liked = args[2]

        if post_author != user_liked:
            db_post.Post.like(post_author, post_id, user_liked)

        self.redirect("/post" "/%s/%s" % (post_author, post_id))
