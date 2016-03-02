__author__ = 'jon'


import tornado.web


class DefaultHandler(tornado.web.RequestHandler):
    """
    Default handler for /
    """

    def get(self, *args, **kwargs):
        self.write(dict(api_version="1.0"))