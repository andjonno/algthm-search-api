"""
Generates a database connection pool. To prevent a pool from being allocated
every time this module is included,
the singleton decorator is added.

When a database connection is required, instantiate the Database class and call
get_connection.
"""

from pymongo import MongoClient
from search.cfg.loader import cfg
from search.core.util.object import singleton


@singleton
class MongoConnection(object):
    """
    Singleton provides database connectivity, specific to running environment.
    """
    __client = None
    __db = None

    def __init__(self):
        if self.__client is None:

            host = cfg.settings.db.host
            port = cfg.settings.db.port

            database = cfg.settings.db.name
            self.__client = MongoClient(
                host=host,
                port=port,
            )
            self.__db = self.__client[database]

    def get_db(self):
        """
        Returns a connection from the pool. It is vitally important that the
        connection is closed once you are finished with it. This allows the
        connection to be returned to the pool, available for other processes.

        :return: mysql.connection
        """
        return self.__db
