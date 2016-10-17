""" Renders login form and validates usernames and passwords

    get(): Renders login form
    post(): Validates username and password and sets authentication cookie

 """
import handler as handler
import helpers.form_data as validate_form # validates user's form data
import helpers.password as pw_hash # creates and validates hashed passwords
import models.user as db_user # facilitates creation and query for users

class Login(handler.Handler):
    """ Renders login screen to user
    and facilitates validation of username and password """
    def get(self):
        self.render("login.html")

    def post(self):
        """ Validate login information with user database record """
        username = self.request.get("username")
        password = self.request.get("password")

        params = dict(username=username)

        if validate_form.username(username) and validate_form.password(password):
            user = db_user.User.by_username(username)
            if user: # if username is valid
                if pw_hash.validate(username, password, user.pw_hash): # if password is valid
                    self.login(user)
                    self.redirect("/welcome")
                    return
        params["login_error"] = "Invalid username or password"
        self.render("login.html", **params)