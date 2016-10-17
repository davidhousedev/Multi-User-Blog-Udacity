""" Routes requests to their requisite handlers """

import webapp2 # Required by Google Cloud Platform for request handling

# Handlers:
import handlers.handler as handler
import handlers.mainpage as mainpage
import handlers.newpost as newpost
import handlers.editpost as editpost
import handlers.deletepost as deletepost
import handlers.viewpost as viewpost
import handlers.likepost as likepost
import handlers.signup as signup
import handlers.login as login
import handlers.logout as logout

# Routes requests to specific handlers
app = webapp2.WSGIApplication([("/new", newpost.NewPost),
                               (r"/post/([a-z, A-Z]+)/([0-9]+)", viewpost.ViewPost),
                               (r"/edit/([a-z, A-Z]+)/([0-9]+)", editpost.EditPost),
                               (r"/del/([a-z, A-Z]+)/([0-9]+)", deletepost.DeletePost),
                               (r"/post/([a-z, A-Z]+)/([0-9]+)/like/([a-z, A-Z]+)", likepost.LikePost),
                               ("/signup", signup.SignUp),
                               ("/login", login.Login),
                               ("/logout", logout.LogOut),
                               (r"/([a-z, A-Z]+)", mainpage.MainPage),
                               (r"/*", mainpage.MainPage),
                              ],
                              debug=True
                              )