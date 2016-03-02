import re


class ResultsProcessor(object):
    """
    ResultsProcessor runs some logic over the results before sending them to
    the user. For example, highlight query terms in the README.
    """

    def __init__(self, query, response):
        self.query = query
        self.response = response

    def run(self):
        """
        Bolds query terms in READMEs
        """
        for result in self.response["results"]:
            self.hl = dict(
                at=[]
            )
            self.canonical_name(result)

            self.highlighting(result)

    def highlighting(self, result):
        readme = result["_source"]["text"]["readme"]
        if not readme:
            return
        query = re.compile("({})".format(self.query.replace(" ", "|")))
        readme = readme.split(" ")

        index = 0
        for word in readme:
            match = re.search(query, word.lower())
            if match:
                self.hl["at"].append([index, match.start(1),
                                      match.end(1) - match.start(1)])
            index += 1
        self.find_summary(result)

    def find_summary(self, result):
        """
        Method finds the section of the readme containing the most query terms.
        """
        def count_range(instances, index, limit):
            """
            Finds number of instances of the query is in range.
            """
            if len(instances) == 0:
                return 0
            count = 0
            for i in instances:
                if index <= i <= limit:
                    count += 1
            return count

        max_index = len(result["_source"]["text"]["readme"].split(" ")) - 1
        index = max = selected = 0
        while index + 40 <= max_index:
            instances = count_range(self.hl["at"], index, index + 40)
            if instances > max:
                selected = index
                max = selected
            index += 1

        self.hl["base"] = selected
        result["_source"]["text"]["_highlighting"] = self.hl

    def canonical_name(self, result):
        split = result["_source"]["repository"]["url"].split("/")
        can_name = split[-2] + "/" + split[-1]
        result["_source"]["repository"]["canonical_name"] = can_name
