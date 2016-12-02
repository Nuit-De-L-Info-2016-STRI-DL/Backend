import json

import tornado

from Handlers.AuthHandler import auth_as_admin
from Handlers.BaseHandler import BaseHandler


class AnnonceHandler(BaseHandler):
    def get(self):
        self.write({"annonces": [json.loads(self.redis_client.lindex("annonces", x))
                                 for x in range(0, 3) if self.redis_client.lindex("annonces", x)]})

    def post(self):
        auth_as_admin()
        data = json.loads(self.request.body.decode('utf-8'))
        gettitle = data['title']
        getdescription = data['description']
        if not gettitle or not getdescription:
            return tornado.web.HTTPError(400, "Bad request")
        self.redis_client.lpush("annonces", json.dumps({'title': gettitle, 'description': getdescription}))
