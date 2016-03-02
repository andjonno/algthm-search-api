
import search.core.db
from datetime import datetime


class QueryLogger:
    """
    QueryLog stores queries in the log store.
    """
    def __init__(self, transaction, query, total_results, response_time,
                 max_score):
        self.db_connection = search.core.db.MongoConnection().get_db()

        # Construct the insertion model
        data = dict(
            transaction=transaction,
            query=query,
            total_results=total_results,
            response_time=response_time,
            timestamp=datetime.today(),
            max_score=max_score
        )
        self.db_connection.query_log.insert(data)



