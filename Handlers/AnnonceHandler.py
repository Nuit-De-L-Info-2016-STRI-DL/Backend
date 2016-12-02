import json

import tornado

from Handlers.AuthHandler import auth_as_admin
from Handlers.BaseHandler import BaseHandler


class AnnonceHandler(BaseHandler):
    def get(self):
        self.write({"annonces": [json.loads(self.redis_client.lindex("annonces", x))
                                 for x in range(0, 3) if self.redis_client.lindex("annonces", x)]})

    @auth_as_admin
    def post(self):
        gettitle = tornado.escape.xhtml_escape(self.get_argument('title'))
        getdescription = tornado.escape.xhtml_escape(self.get_argument('description'))
        self.redis_client.lpush("annonces", json.dumps({'title': gettitle, 'description': getdescription}))
