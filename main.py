#!/usr/bin/env python

import functools

import tornado.web
import tornado.httpserver
import tornado

from models import User, Question

import os

def require_login(method):
    """Decorate with this method to restrict to site admins."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method == "GET":
                self.redirect(self.get_login_url())
                return

            raise tornado.web.HTTPError(403)
        else:
            return method(self, *args, **kwargs)

    return wrapper

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_login_url(self):
        return "/login"

    def render_string(self, template_name, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = ''

        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = []

        return tornado.web.RequestHandler.render_string(
            self, template_name, **kwargs)

class LoginHandler(BaseHandler):
   def get(self):
       self.render("login.html")

   def post(self):
       username = self.get_argument('username', None)
       password = self.get_argument('password', None)

       if not username or not password:
           self.render("login.html", message="Username/Password is empty")
           return

       user = User.one({'username': username})

       if not user:
           self.render("login.html", message="Invalid Username/Password")
           return

       if not user.verify_password(password):
           self.render("login.html", message="Invalid Username/Password")
           return

       self.set_secure_cookie("user", username)
       self.redirect("/")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        confirm_password = self.get_argument('confirm_password', None)

        first_name = self.get_argument('first_name', None)
        last_name = self.get_argument('last_name', None)

        messages = []

        if not username:
            messages.append("Username is empty")

        if not password:
            messages.append("Password is empty")

        if not first_name:
            messages.append("First name is empty")

        if not last_name:
            messages.append("Last name is empty")
  
        if password != confirm_password:
            messages.append("Passwords are not equal")

        if len(password) < 6:
            messages.append("Password length must be bigger than 6 chars")

        user = User.one({'username': username})

        if user:
            messages.append('Username must be unique. %s is already take' % username)

        if len(messages) != 0:
            self.render("register.html", error_messages=messages)
            return

        user = User()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)

        user.save(validate=True)

        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")

class HomeHandler(BaseHandler):
    def get(self):
        self.render("index.html")

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "11oETzKXQAGaedkLxgEmEeJJ4uYh7EQnp2XdTP1o/Vo=",
    "xsrf_cookies": True,
    "debug": True
}

application = tornado.web.Application([
    (r"/login/?", LoginHandler),
    (r"/logout/?", LogoutHandler),
    (r'/register/?', RegisterHandler),
    (r"/", HomeHandler)
], **settings)
        
def main():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    print "Running application on port 8000"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt, e:
        pass
