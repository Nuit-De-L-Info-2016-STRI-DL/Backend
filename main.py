#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string

import redis
import tornado.web
import tornado.httpserver
from tornado.options import define, options

from Handlers.APIHandler import CommonAPIHandler
from Handlers.AnnonceHandler import AnnonceHandler
from Handlers.MainHandler import MainHandler
from Handlers.AuthHandler import LoginHandler
from Handlers.ChatHandler import ChatSocketHandler, ChatHandler
from Handlers.BaseHandler import BaseHandler
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# app's title
__title__ = 'Dashboard API'

define("port", default=8080, help="run on the given port", type=int)
define("redis_host", default="127.0.0.1", help="redis database host")
define("redis_port", default="6379", help="redis database port")
define("redis_database", default=0, help="redis database name", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path': './static',
            'template_path': './templates',
            'cookie_secret': ''.join([random.choice(string.printable) for _ in range(64)]),
            'login_url': '/auth/login',
            #'xsrf_cookies': True,
        }
        # create an app instance
        handlers = [
            (r'/', MainHandler),  # index.html
            (r'/api(.*)$', CommonAPIHandler),
            (r'/auth(.*)$', LoginHandler),
            (r'/chatsocket(.*)$', ChatSocketHandler),
            (r'/chat(.*)$', ChatHandler),
            (r'/annonce', AnnonceHandler),
            (r'/.*', BaseHandler),
        ]
        super(Application, self).__init__(handlers, **settings)
        self.redis_client = redis.Redis(host=options.redis_host, port=options.redis_port, db=options.redis_database,
                              charset="utf-8", decode_responses=True)

        self.maybe_init_redis()

    def maybe_init_redis(self):
        if not self.redis_client.get("users-admin"):
            print("Create user admin")
            # create default admin user
            self.redis_client.set("users-admin",
                        tornado.escape.utf8(LoginHandler.hash_password("admin")))
            self.redis_client.set('usersisadmin-admin', True)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print("Server Listen {}".format(options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
