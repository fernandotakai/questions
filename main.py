#!/usr/bin/env python

import functools

import tornado.web
import tornado.httpserver
import tornado

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
    "xsrf_cookies": False
}

application = tornado.web.Application([
    (r"/login/?", LoginHandler),
    (r"/logout/?", LogoutHandler),
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
