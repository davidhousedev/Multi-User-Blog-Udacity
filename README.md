#Multi-User Blog

This blog site allows for the creation of text blogs authored to different users. Users can comment on, edit, and like blog posts. The site is fully responsive and supports all screen sizes. It was developed specifically for implementation on Google's Cloud Platform.

This project was developed as a part of the Udacity Full Stack Nanodegree program.

## Modules and Frameworks

* __main.py__ - Imports handlers and routes requests
* __handlers__ - Contains all request handlers
  * __deletepost.py__ - Queries Database for a specified post. If found, deletes that post
  * __editpost.py__ - Renders post edit form, and writes edits to database
  * __handler.py__ - This handler contains methods used across many pages. All other handlers inherit form this class.
  * __likepost.py__ - Facilitates liking and unliking of posts
  * __login.py__ - Renders login form and validates usernames and passwords
  * __logout.py__ - Clears authentication cookie
  * __mainpage.py__ - Renders home page, showing all blogs posted by all users
  * __newpost.py__ - Renders form for writing a new post, and writes post to database
  * __signup.py__ - Renders form for creating new users, and writes new users to database
  * __viewpost.py__ - Displays a single post, and facilitates post comment creation
* __helpers__ - Functions to assist with primary application flow
  * __cookie.py__ - Creates and validates secure cookies using HMAC encryption and a server-define secure secret.
    * __hmac__ - Encrypts user authentication cookies with a server secret
  * __cookie_secret.py__ - Contains a simple function for returning a secret phrased used in cookie.py HMAC encryption. **You must set your own secret on your server, and exclude this file from any public git repository**.
  * __form_data.py__ - Validates form input usernames and passwords according to corresponding regular expressions (RegEx).
    * __re__ - Reads regular expressions in URL paths and form data validation
  * __password.py__ - Creates and validates encrypted password hashes, with unique salts, for writing to a database.
    * __random__ - Creates random chars for use in password salts
    * __hashlib__ - Facilitates encryption of password hashes
    * __string__ - Populates a list of letters used when creating password salts
* __models__ - Database model classes for facilitating database operations with Google Cloud Datastore
  * __google.appengine.ext: db__ - Facilitates all database operations
  * __comment.py__ - A Comment entity will contain the text of a comment to a blog post. Comments must be defined with a blog post as a parent.
  * __post.py__ - A Post entity will facilitate the creation, writing, and querying of blog posts in the database. Blog posts must be defined with a User as a parent.
  * __user.py__ - A User entity allows a user to log in, log out, create blog posts, and comment. Users do not require parents.
* __Grunt__ - This project utilizes the Grunt task runner to concatenate and minify CSS files from /static to /static/dist.
* __Bootstrap__ - The Bootstrap css framework is used extensively to make the site responsive.
* __os__ - Facilitates aquisition of Jinja2 templates from server directory
* __Jinja2__ - HTML Templating framework
* __re__ - Reads regular expressions in URL paths


## Installation

###Requirements:
  * Python 2.7.9
  * Google Cloud SDK and Python components: https://cloud.google.com/sdk/downloads

1. Download and install Google Cloud SDK
2. Use SDK to install Python components
3. Initiate your SDK with a google account and an app engine project
4. Clone this repository
5. Run the app
  * Locally:
    1. Navigate to your cloned repo's directory
    2. run: `dev_appserver.py ./`
      * App will be accessable at `localhost:8080`
      * Local datastore will be at `localhost:8000/datastore`
  * Online:
    1. Deploy app to your project by running `gcloud app deploy`
    2. Run `gcloud app browse` to open an window to your project
      * Cloud datastore will be accessable through your google cloud console
6. Optional: Install grunt at [http://gruntjs.com/getting-started](http://gruntjs.com/getting-started)
  * Run `grunt watch` from repo directory to automatically re-minify CSS changes to minified CSS, whenever changes are made
  * Run `grunt` to manually re-minify CSS

## Author

David A. House
davidhousedev
davidhousedev@gmail.com


## License

Copyright (c) 2016 David Alexander House

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.