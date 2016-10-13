import os

import jinja2 # HTML Templating framework
import webapp2 # Required by Google Cloud Platform for request handling

import models.post as db_post
import helpers.data_validation as validate

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

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
        with any number of vars (params1+) """
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    """ Default HTTP Request Handler """
    def get(self):
        """ Display 10 most recent blog posts """

        posts = db_post.Post.view_posts(10)

        self.render("allblogs.html", posts=posts)

class NewPost(Handler):
    """ Handles all requests related to creating new blog posts """
    def show_form(self, form_data=None):
        """ Display HTML form with any residual user-generated content """
        self.render("newpost.html", form_data=form_data)

    def get(self):
        """ Show form without any user data """
        self.show_form()

    def post(self):
        """ If user input from form is valid, create new blog post in database """
        form_data = {}
        form_data["title"] = self.request.get("title")
        form_data["content"] = self.request.get("content")

        if form_data["title"] and form_data["content"]:
            new_post = db_post.Post(title=form_data["title"],
                                    content=form_data["content"])
            #TODO: Add author to creation of blog post
            new_post.put()
        else:
            form_data["error"] = "Both a title and content are required"
            self.show_form(form_data)

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
        error_flag = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username=username,
                      email=email)
        if not validate.username(username):
            params["error_username"] = "That is not a valid username"
            error_flag = True

        if not validate.password(password):
            params["error_password"] = "That is not a valid password"
            error_flag = True
        elif password != verify:
            params["error_verify"] = "Passwords do not match"
            error_flag = True

        if not validate.email(email):
            params["error_email"] = "That is not a valid email"
            error_flag = True

        if error_flag:
            self.render("signup.html", **params)
        else:
            #TODO: Write valid user to db
            raise NotImplementedError








# Routes requests to specific handlers
app = webapp2.WSGIApplication([("/", MainPage),
                               ("/new", NewPost),
                               ("/signup", SignUp),
                              ],
                              debug=True
                              )