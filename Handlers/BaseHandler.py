import tornado


class BaseHandler(tornado.web.RequestHandler):
    """Superclass for Handlers which require a connected user
    """

    @property
    def redis_client(self):
        return self.application.redis_client


    def get_current_user(self):
        """Get current connected user
        :return: current connected user
        """
        return self.get_secure_cookie("user")

        def write_error(self, status_code, **kwargs):
            if status_code == 404:
                self.render('404.html'<Plug>PeepOpenage=None)
            else:
                self.write('oupsss...')
                return
