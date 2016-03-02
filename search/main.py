"""
Entry Point for the Search API.
"""

import tornado.web
from search.controllers import DefaultHandler
from search.controllers import query_handler
from search.controllers import metric_handler
from search.controllers import autosuggest
from logger import logger
from cfg.loader import cfg

# ------------------------------------------------------------------------------
#   Configure Logging
# ------------------------------------------------------------------------------
logger.setup_logging()
logger = logger.get_logger('search_api')

# ------------------------------------------------------------------------------
#   Configure Application
# ------------------------------------------------------------------------------
application = tornado.web.Application(
    [
        (r"/", DefaultHandler),
        (r"/query", query_handler.QueryHandler),
        (r"/metrics/([A-z0-9]+)", metric_handler.MetricHandler),
        (r"/_auto", autosuggest.AutoSuggest),
    ]
    , debug=True)


def main():
    logger.info('Booting Search API ..')
    port = cfg.settings.general.port
    logger.info('Binding to port {}'.format(port))
    logger.info('DB Connection for Mongo @ {}:{}'.format(cfg.settings.db.host,
                                             cfg.settings.db.port))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()