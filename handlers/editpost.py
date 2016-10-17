""" Renders post edit form, and writes edits to database

    get(self, author, post_id): Renders a form for editing a post
    post(self, author, post_id): Sends post edit information to database, where it is written

 """

import handler as handler
import models.post as db_post # facilitates creation and query for blog posts

class EditPost(handler.Handler):
    """ Renders post editing form,
    and writes post edits to database """
    def get(self, author, post_id):
        """ Open html view used to edit post """
        if not self.user:
            self.redirect("/login")

        post = db_post.Post.get_post(author, post_id)
        if post and self.user.username == author:
            self.render("editpost.html", post=post)

    def post(self, author, post_id):
        """ If current user is author,
        edit posts according to changes made in edit view """
        if not self.user:
            self.redirect("/login")

        if self.user.username == author:
            title = self.request.get("title")
            content = self.request.get("content")

            db_post.Post.edit(author, post_id, title, content)
            self.redirect("/post" "/%s/%s" % (author, post_id))
            return
        self.redirect("/post" "/%s/%s" % (author, post_id))