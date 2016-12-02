import logging

import bcrypt
import tornado
from tornado import concurrent
from tornado import gen

from Handlers.BaseHandler import BaseHandler


def auth_as_admin():
    @tornado.web.authenticated
    def func_wrapper(self):
        isadmin = self.redis_client.get("usersisadmin-" + self.get_current_user().decode("utf-8"))
        if not isadmin or isadmin.lower() != "true":
            return tornado.web.HTTPError(403, "Forbidden")
    return func_wrapper


class LoginHandler(BaseHandler):
    executor = concurrent.futures.ThreadPoolExecutor(2)

    @gen.coroutine
    def get(self, path_request):
        """Get login form
        """
        if path_request == '/login':
            incorrect = self.redis_client.get(self.request.remote_ip)
            if incorrect and int(incorrect) > 5:
                logging.warning('an user have been blocked')
                self.write('<center>blocked</center>')
                return
            self.render('login.html', user=self.current_user)
        elif path_request == '/logout':
            self.clear_cookie('user')
            self.redirect('/')
        elif path_request == '/register':
            auth_as_admin()
            self.render('register.html', user=self.current_user)
        else:
            self.send_error(status_code=400, reason='bad request')

    @gen.coroutine
    def post(self, path_request):
        """Post connection form and try to connect with these credentials
        """
        if path_request == '/login':
            getusername = tornado.escape.xhtml_escape(self.get_argument('username'))
            getpassword = tornado.escape.xhtml_escape(self.get_argument('password'))

            password = self.redis_client.get('users-' + getusername)

            hashed_password = None
            if password:
                hashed_password = yield LoginHandler.executor.submit(
                    bcrypt.hashpw, tornado.escape.utf8(getpassword),
                    tornado.escape.utf8(password))

            if hashed_password and hashed_password.decode('utf-8') == password:
                self.set_secure_cookie("user", getusername, expires_days=1)
                self.redis_client.delete(self.request.remote_ip)
                self.redirect('/')
            else:
                logging.info('invalid credentials')
                incorrect = self.redis_client.get(self.request.remote_ip)
                self.redis_client.setex(self.request.remote_ip, (int(incorrect) + 1 if incorrect else 1), 3600 * 24)
                self.render('login.html', user=self.current_user)
        elif path_request == '/register':
            auth_as_admin()
            getusername = tornado.escape.xhtml_escape(self.get_argument('username'))
            getpassword = tornado.escape.xhtml_escape(self.get_argument('password'))
            getisadmin = tornado.escape.xhtml_escape(self.get_argument('isadmin', 'False'))

            if len(getpassword) < 8:
                raise tornado.web.HTTPError(400, "Bad Parameter")

            self.redis_client.set('users-' + getusername,
                                  (yield LoginHandler.executor.submit(LoginHandler.hash_password, getpassword)))
            self.redis_client.set('usersisadmin-' + getusername, getisadmin.lower() == "True")
        else:
            self.send_error(status_code=400, reason='bad request')

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(tornado.escape.utf8(password), bcrypt.gensalt())

