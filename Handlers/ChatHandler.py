import json
import logging
import uuid

import tornado.web
import tornado.websocket
import tornado.escape

from Handlers import AuthHandler
from Handlers.BaseHandler import BaseHandler


class ChatHandler(BaseHandler):
    def get(self, path_request):
        if path_request == '/chat':
            self.render('chat.html', messages=[])
        else:
            self.send_error(status_code=400, reason='bad request')



class ChatSocketHandler(tornado.websocket.WebSocketHandler, BaseHandler):
    def initialize(self):
        self.subscrib = self.redis_client.pubsub()
        self.thread = None

    def get_compression_options(self):
        return {}  # Non-None enables compression with default options.

    def open(self, path_request):
        self.channel = 'messages' + path_request[:1]
        if path_request not in ['/general', '/dormir', '/manger', '/soins', '/demarche', '/as', '/admin']:
            raise tornado.web.HTTPError(404, "Bad request")
        elif path_request == '/admin':
            AuthHandler.auth_as_admin()
        elif path_request == '/as':  # connected
            if not self.get_current_user():
                return tornado.web.HTTPError(403, "Forbidden")
        self.subscrib.subscribe(**{self.channel: self.send_updates})
        self.thread = self.subscrib.run_in_thread(sleep_time=0.001)

    def on_close(self):
        self.subscrib.unsubscribe(self.channel)
        self.thread.stop()

    def send_updates(self, chat):
        try:
            self.write_message(chat['data'])
        except tornado.websocket.WebSocketClosedError:
            logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            'id': str(uuid.uuid4()),
            'body': parsed['body'],
        }
        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))
        self.redis_client.publish(self.channel, json.dumps(chat))
