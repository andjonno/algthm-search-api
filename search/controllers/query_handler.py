import tornado.web
from search.logger import logger
from search.core.query_log import QueryLogger
from datetime import datetime
import requests
from search.core.query_preprocessor import QueryPreProcessor
from uuid import uuid4
from search.cfg.loader import cfg
from search.core.results_processor import ResultsProcessor
import json


logger = logger.get_logger('search_api')


class QueryHandler(tornado.web.RequestHandler):
    """
    QueryHandler responds to queries passed from the web front end.
    """

    def get(self, *args, **kwargs):
        self.transaction_id = uuid4().hex
        self.query = self.get_argument("q", False)
        self.from_position = self.get_argument("from", 0)

        self.__log("Processing")

        if self.query:
            self.begin_transaction()
            self.query = QueryPreProcessor(self.query).process().get_result()

            try:
                self.request_from_index()
            except requests.ConnectionError as e:
                logger.error("Index connection error. {}".format(e))
                self.response = dict(
                    error="Search unavailable at this time. Try again later."
                )
                self.write(self.response)
                self.finish()

            # Process results
            ResultsProcessor(self.query, self.response).run()

            self.commit_transaction()
            self.set_header("Access-Control-Allow-Origin",
                            "http://algthm.io:8080")
            self.write(self.response)
            self.__log("Time Taken {}s".format(self.response_time))
            self.__log("{} results".format(self.total_results))
            self.__log("Done")
            self.finish()

        else:
            self.write(dict(error="query empty"))

    def begin_transaction(self):
        """
        Marks the beginning of the query transaction by saving the current
        time.

        :return: None
        """
        self.start = datetime.today()

    def commit_transaction(self):
        """
        Marks the end of the transaction. Calculates query time and requests a
        save from the query log asynchronously.
        Queries are only logged from 0, not successive calls for results.
        :return:
        """
        self.response_time = (datetime.today() - self.start).total_seconds()
        self.response["response_time"] = self.response_time

        if self.from_position == 0:
            QueryLogger(transaction=self.transaction_id,
                        query=self.query,
                        total_results=self.total_results,
                        response_time=self.response_time,
                        max_score=self.max_score)

    def request_from_index(self):
        data = dict(
            query=dict(
                query_string=dict(
                    query=self.query
                )
            ),
            sort=[dict(
                # _score=dict(order="desc"),
                # algthm_score=dict(order="desc"),
            )],
            # "from"=self.from_position,
            # size=cfg.settings.general.result_size
        )
        # data = {
        #     "filtered" : {
        #         "query" : {
        #             "queryString" : {
        #                 "default_field" : "readme",
        #                 "query" : "ruby"
        #             }
        #         }
        #     }
        # }
        """
        Makes a call to the index with the users query.
        :return: Response dictionary
        """
        url = "http://localhost:9200/algthm/_search"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        response = r.json()

        try:
            self.max_score = response["hits"]["max_score"]
            self.response = dict(
                transaction=self.transaction_id,
                query=self.query,
                results=response["hits"]["hits"],
                total_results=response["hits"]["total"],
                max_score=self.max_score
            )
            self.total_results = response["hits"]["total"]

        except Exception:
            return dict(message="error")

    def __log(self, message=""):
        """
        Proxy for logger.info
        :return: None
        """
        logger.info("[{} - \"{}\"] - {}".format(self.transaction_id, self.query,
                                            message))
