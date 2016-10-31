# -*- coding: utf-8 -*-

import os
import subprocess
import random
import json
import tornado.web
import tornado.escape

daemon_folder = './Daemons'
correct_actions = {'stop', 'start', 'restart', 'status', 'run-once'}


def check_status_daemon(daemon_pid_file: str):
    try:
        with open(daemon_pid_file, mode='r', encoding='UTF-8') as pf:
            if int(pf.read().strip()):
                return True
    except IOError:
        pass
    return False


class CommonAPIHandler(tornado.web.RequestHandler):
    """
    Class to handle '/api' endpoint.
    """

    def get(self, path_request):
        """
        Handle GET requests.

        :param path_request: request path ( < URI)
        """
        if path_request == '/random':
            self.write(str(random.randint(0, 100)))
        elif path_request == '/abspath':
            self.write(os.path.abspath('.'))
        elif path_request == '/status':
            self.write(json.dumps([
                    {'Name': '', 'Status': check_status_daemon('/tmp/test.pid')},
                ]))
        else:
            self.send_error(status_code=400, reason='bad request')

    def post(self, path_request):
        """
        Handle POST requests.

        :param path_request: request path ( < URI)
        """
        if path_request == '/daemon-control':
            name = self.get_argument('name')
            action = self.get_argument('action')
            if action not in correct_actions:
                self.send_error(status_code=400, reason='bad request')
                return
            if name == 'Test':
                subprocess.check_call(['python', 'Test.py', action], cwd=daemon_folder)
            else:
                self.send_error(status_code=400, reason='bad request')
                return
        else:
            self.send_error(status_code=400, reason='bad request')
        return
