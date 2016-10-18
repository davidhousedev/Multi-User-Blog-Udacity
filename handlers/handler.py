""" This handler contains methods used across many pages.
All other handlers inherit form this class.

    Methods:
        write(self, *a, **kw) - Renders html templates with Jinja2 variables
        render_str(self, template, **params) - Finds specified template in '/template' of current dir
        render(self, template, **kw) - Finds specified template in '/template' of current dir
        set_secure_cookie(self, name, val) - Creates, and sets a secure cookie
        read_secure_cookie(self, name) - Reads, then validates the user cookie param:name
        login(self, user) - Sends secure cookie to browser according to current user
        logout(self) - Clears current authentication cookie
        initialize(self, *a, **kw) - Run by Webapp2 on every page load, queries db for current user

"""
import os
import jinja2  # HTML Templating framework
import webapp2  # Required by Google Cloud Platform for request handling

import models.user as db_user  # facilitates creation and query for users

import helpers.cookie as cookie  # creates and validates authentication cookies


# Jinja environment logic sourced from Intro to Backend course material
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../templates')
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
        self.user = db_user.User.by_username(username)