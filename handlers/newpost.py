""" Renders form for writing a new post, and writes post to database

    get(): Renders form for writing a new post
    post(): Sends changes to database

"""

import handler as handler
import models.post as db_post # facilitates creation and query for blog posts

class NewPost(handler.Handler):
    """ Handles all requests related to creating new blog posts """
    def show_form(self, form_data=None):
        """ Display HTML form with any residual user-generated content """
        self.render("newpost.html", form_data=form_data)

    def get(self):
        """ Show form without any user data """
        if self.user:
            self.show_form()
        else:
            self.redirect("/login")

    def post(self):
        """ If user input from form is valid, create new blog post in database """
        if not self.user:
            self.redirect("/login")

        form_data = {}
        form_data["title"] = self.request.get("title")
        form_data["content"] = self.request.get("content")

        if form_data["title"] and form_data["content"]:
            new_post = db_post.Post(parent=self.user,
                                    author=self.user.username,
                                    title=form_data["title"],
                                    likes=0,
                                    users_liked=[],
                                    content=form_data["content"])
            new_post.put()
            self.redirect("/post/%s/%s" %(self.user.username,
                                          new_post.key().id()))
        else:
            form_data["error"] = "Both a title and content are required"
            self.show_form(form_data)