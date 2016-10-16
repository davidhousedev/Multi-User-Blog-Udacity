import os

import jinja2 # HTML Templating framework
import webapp2 # Required by Google Cloud Platform for request handling

import models.post as db_post
import models.user as db_user
import models.comment as db_comment
import helpers.cookie as cookie
import helpers.form_data as validate_form
import helpers.password as pw_hash

# Jinja environment logic sourced from Intro to Backend course material
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

# Methods in Handler class are all sourced from Intro to Backend course material
class Handler(webapp2.RequestHandler):
    """ Renders html templates with Jinja2 variables """
    def write(self, *a, **kw):
        """ Writes HTML """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ Finds specified template in '/template' of current dir """
        template = JINJA_ENV.get_template(template)
        return template.render(params)

    def render(self, template, **kw):
        """ Render a specific template (param0)
        with any number of vars and the current user (if logged in) """
        if self.user:
            kw["current_user"] = self.user.username
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """ Creates, then sends to user, a secure cookie of "name=val|hash" """
        cookie_val = cookie.make(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """ Reads, then validates the user cookie param:name """
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            no_hash_val = cookie.validate(cookie_val)
            if no_hash_val:
                return no_hash_val

    def login(self, user):
        """ Sends secure cookie to browser according to current user """
        self.set_secure_cookie('username', user.username)

    def logout(self):
        """ Clears current authentication cookie """
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')

    def initialize(self, *a, **kw):
        """ On every page load, searches for and reads any user authentication cookie
        If found, queries database for record of that user to store in self.user """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        username = self.read_secure_cookie('username')
        self.user = db_user.User.by_name(username)

class MainPage(Handler):
    """ Default HTTP Request Handler """
    def get(self):
        """ Display 10 most recent blog posts """

        posts = db_post.Post.view_posts(10)

        # Get the number of comments for each post,
        # and store as int in each post.
        for post in posts:
            comment_arry = db_comment.Comment.get_comments(post)
            post.num_comments(len(comment_arry))

        self.render("allblogs.html", posts=posts, user=self.user)

class NewPost(Handler):
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
                                    users_liked = [],
                                    content=form_data["content"])
            new_post.put()
            self.redirect("/post/%s/%s" %(self.user.username,
                                          new_post.key().id()))
        else:
            form_data["error"] = "Both a title and content are required"
            self.show_form(form_data)

class EditPost(Handler):
    """ Renders post editing form,
    and writes post edits to database """
    def get(self, author, post_id):
        if not self.user:
            self.redirect("/login")

        post = db_post.Post.get_post(author, post_id)
        if post and self.user.username == author:
            self.render("editpost.html", post=post)

    def post(self, author, post_id):
        if not self.user:
            self.redirect("/login")

        if self.user.username == author:
            title = self.request.get("title")
            content = self.request.get("content")

            db_post.Post.edit(author, post_id, title, content)
            self.redirect("/post" "/%s/%s" % (author, post_id))
            return
        self.redirect("/")



class ViewPost(Handler):
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

class LikePost(Handler):
    """ Increase post likes by 1 """
    def get(self, *args):
        post_author = args[0]
        post_id = args[1]
        user_liked = args[2]

        if post_author != user_liked:
            db_post.Post.like(post_author, post_id, user_liked)

        self.redirect("/post" "/%s/%s" % (post_author, post_id))




class SignUp(Handler):
    """ Handles all requests pertaining to signing up new users """
    def show_form(self, form_data=None):
        """ Display HTML form with any residual user-generated content """
        self.render("signup.html", form_data=None)

    def get(self):
        """ Show form without any user data """
        self.show_form()

    def post(self):
        """ If user input from form is valid, create new user in database """
        # Logic inspired by Intro to Backend course materials
        #TODO: Abstract away this code to form_data.py
        error_flag = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username,
                      email=email)

        if not validate_form.username(username):
            params["error_username"] = "That is not a valid username"
            error_flag = True

        if db_user.User.by_name(username):
            params["error_username"] = "That user already exists"
            error_flag = True

        if not validate_form.password(password):
            params["error_password"] = "That is not a valid password"
            error_flag = True
        elif password != verify:
            params["error_verify"] = "Passwords do not match"
            error_flag = True

        if not validate_form.email(email):
            params["error_email"] = "That is not a valid email"
            error_flag = True

        if error_flag:
            self.render("signup.html", **params)
        else:
            hashed_pw = pw_hash.make(username, password)
            usr = db_user.User.register(username, hashed_pw, email)
            self.set_secure_cookie("username", usr.username)
            self.redirect("/")

class Login(Handler):
    """ Renders login screen to user
    and facilitates validation of username and password """
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        params = dict(username=username)

        if validate_form.username(username) and validate_form.password(password):
            user = db_user.User.by_name(username)
            if user:
                if pw_hash.validate(username, password, user.pw_hash):
                    self.login(user)
                    self.redirect("/")
                    return
        params["login_error"] = "Invalid username or password"
        self.render("login.html", **params)

class LogOut(Handler):
    def get(self):
        self.logout()
        self.redirect("/")











# Routes requests to specific handlers
app = webapp2.WSGIApplication([("/", MainPage),
                               ("/new", NewPost),
                               (r"/post/([a-z, A-Z]+)/([0-9]+)", ViewPost),
                               (r"/edit/([a-z, A-Z]+)/([0-9]+)", EditPost),
                               (r"/post/([a-z, A-Z]+)/([0-9]+)/like/([a-z, A-Z]+)", LikePost),
                               ("/signup", SignUp),
                               ("/login", Login),
                               ("/logout", LogOut),
                              ],
                              debug=True
                              )