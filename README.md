#Multi-User Blog
This is the third project for the Udacity Full Stack Web Developer Nanodegree.

## Modules

*__main.py__ - Facilitates request handling, routing, form processing, and database operations
  *__os__ - Facilitates aquisition of Jinja2 templates from server directory
  *__Jinja2__ - HTML Templating framework
  *__re__ - Reads regular expressions in URL paths
*__helpers__ - Functions to assist with primary application flow
  *__cookie.py__ - Creates and validates secure cookies using HMAC encryption and a server-define secure secret.
    *__hmac__ - Encrypts user authentication cookies with a server secret
  *__cookie_secret.py__ - Contains a simple function for returning a secret phrased used in cookie.py HMAC encryption. **You must set your own secret on your server, and exclude this file from any public git repository**.
  *__form_data.py__ - Validates form input usernames and passwords according to corresponding regular expressions (RegEx).
    *__re__ - Reads regular expressions in URL paths and form data validation
  *__password.py__ - Creates and validates encrypted password hashes, with unique salts, for writing to a database.
    *__random__ - Creates random chars for use in password salts
    *__hashlib__ - Facilitates encryption of password hashes
    *__string__ - Populates a list of letters used when creating password salts
*__models__ - Database model classes for facilitating database operations with Google Cloud Datastore
  *__google.appengine.ext: db__ - Facilitates all database operations
  *__comment.py__ - A Comment entity will contain the text of a comment to a blog post. Comments must be defined with a blog post as a parent.
  *__post.py__ - A Post entity will facilitate the creation, writing, and querying of blog posts in the database. Blog posts must be defined with a User as a parent.
  *__user.py__ - A User entity allows a user to log in, log out, create blog posts, and comment. Users do not require parents.


## License
Read: LICENSE

## Installation
