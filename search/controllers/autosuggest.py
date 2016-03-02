import tornado.websocket
from search.logger import logger
from uuid import uuid4
from datetime import datetime
from search.core.db import MongoConnection

logger = logger.get_logger('search_api')


class AutoSuggest(tornado.websocket.WebSocketHandler):

    def open(self):
        self.time = datetime.today()
        self.id = uuid4().hex
        self.db = MongoConnection().get_db()
        logger.info("auto-suggestion established [{}]".format(self.id))

    def on_message(self, message):
        if (datetime.today() - self.time).total_seconds() >= 1 and message != "":
            logger.info("processing suggestions: [\"{}\", \"{}\"]".format(self.id, message))
            self.time = datetime.today()
            self.write_message(self.get_suggestions(message))

    def get_suggestions(self, query):
        """
        Query mongo, query_log for now but will move to more efficient reduced
        table - this is fine for now.

        the query:
        db.query_log.aggregate([
            { $match: { query: /ja/ } },
            { $group: { _id: "$query", total: { $sum: 1 } } },
            { $sort: { total: -1 } },
            { $limit: 4 }
        ])

        :param query:
        :return:
        """

        response = dict(
            query=query,
            suggestions=[]
        )

        results = self.db.query_log.aggregate([
            {"$match": {"query": {"$regex": "^{}".format(query)}}},
            {"$group": {"_id": "$query", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}},
            {"$limit": 4}
        ])

        # top rank is first result
        if len(results["result"]):

            max = results["result"][0]["total"]

            # normalize data
            for result in results["result"]:
                result["rank"] = result["total"] / (max * 1.0)
                result["suggestion"] = result["_id"]
                del result["total"]
                del result["_id"]

                response["suggestions"].append(result)

        return response