#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from Handlers.APIHandler import CommonAPIHandler
from Handlers.MainHandler import MainHandler
from Handlers.DataAPIHandler import DataAPIHandler
from tools import server


# app's title
__title__ = 'Dashboard API'


def main():
    # define app's settings
    settings = {
        'static_path': './static',
        'template_path': './templates',
    }
    # create an app instance
    application = tornado.web.Application([
            (r'/', MainHandler),  # index.html
            (r'/data/(.*)$', DataAPIHandler),
            (r'/api(.*)$', CommonAPIHandler),
        ], **settings)
    # launch it in a new http server
    server.start_http(app=application, http_port=8080)


if __name__ == '__main__':
    main()
