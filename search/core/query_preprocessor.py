

class QueryPreProcessor:
    """
    Query pre-processor. Prepares the query before querying against the index.
    """

    def __init__(self, query=None):
        if not query:
            raise ValueError('Query:string missing.')

        self.query = query
        self.process()

    def process(self):
        """
        Run processes here.
        :return:
        """
        # TODO: Process query
        self.query = self.query

        return self

    def get_result(self):
        """
        Deliver outcome.
        :return: Query:string
        """
        return self.query
