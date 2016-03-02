import tornado.web
from search.core.db import MongoConnection
from bson.objectid import ObjectId, InvalidId


class MetricHandler(tornado.web.RequestHandler):

    def get(self, _id):
        # pagination
        skip = int(self.get_argument("next", 0))
        if not _id:
            self.write(dict(
                error="Repository ID required."
            ))
        try:
            _id = ObjectId(_id)
        except InvalidId:
            self.write(dict(
                error="Invalid ID"
            ))

        db = MongoConnection().get_db()
        response = dict(
            metrics=[],
            contributors=[],
        )

        metrics = db.metrics.find({'repository.$id': _id})\
            .skip(skip)\
            .sort("timestamp", -1)\
            .limit(4)
        for result in metrics:
            del result["repository"]
            result["timestamp"] = str(result["timestamp"])
            result["_id"] = str(result["_id"])
            response["metrics"].append(result)

        contributors = db.contributions.find({"repository.$id": _id})\
            .sort("contributions", -1)\
            .limit(15)
        for result in contributors:
            contributor = dict(
                name=result["name"],
                email=result["email"]
            )
            response["contributors"].append(contributor)

        self.set_header("Access-Control-Allow-Origin", "http://algthm.io:8080")
        self.write(response)
