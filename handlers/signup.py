""" Renders form for creating new users, and writes new users to database

    get(): Renders new user signup form
    post(): If user input is valid, creates new user

"""


import handler as handler
import models.user as db_user # facilitates creation and query for users
import helpers.form_data as validate_form # validates user's form data
import helpers.password as pw_hash # creates and validates hashed passwords

class SignUp(handler.Handler):
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

        if not validate_form.username(username):
            params["error_username"] = "That is not a valid username"
            error_flag = True

        if db_user.User.by_username(username):
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
            self.redirect("/welcome")