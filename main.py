import os

import jinja2 # HTML Templating framework
import webapp2 # Required by Google Cloud Platform for request handling

import models.post as db_post

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
        """ Handle GET requests """
        self.render("index.html")

class NewPost(Handler):
    """ Handles all requests related to creating new blog posts """
    def show_form(self, form_data=None):
        """ Display HTML form with any residual user-generated content """
        self.render("newpost.html", form_data=form_data)

    def get(self):
        """ Show form without any user data """
        self.show_form()

    def post(self):
        form_data = {}
        form_data["title"] = self.request.get("title")
        form_data["content"] = self.request.get("content")

        if form_data["title"] and form_data["content"]:
            new_post = db_post.Post(title=form_data["title"],
                                    content=form_data["content"])
            new_post.put()
        else:
            form_data["error"] = "Both a title and content are required"

# Routes requests to specific handlers
app = webapp2.WSGIApplication([("/", MainPage),
                               ("/new", NewPost),
                              ],
                              debug=True
                              )