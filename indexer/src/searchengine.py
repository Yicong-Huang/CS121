import math
from datetime import datetime
from functools import reduce


class SearchEngine:
    HTTP = "http://"

    # Todo: add search based on distance of documents
    def __init__(self, store):
        self._token_store = store
        self.book = self._token_store.get_bookkeeping()
        self.document_count = self._token_store.get_document_count()

    @staticmethod
    def _score_position(first: [int], second: [int], *args):
        params = [first, second, *args]
        score = 0
        if args:
            for pos in first:
                result = (pos + 1) in second
                for i in range(len(args)):
                    result &= (pos + i + 2) in args[i]
                score += result
            return score + SearchEngine._score_position(*params[:len(params) - 1]) + SearchEngine._score_position(
                *params[1:])
        else:
            for pos in first:
                score += (pos + 1) in second
            return score

    def search(self, queries: list, limit=10):
        time = datetime.now()
        if len(queries) > 1:
            print("MULTIPLE WORD SEARCH START")
            all_token_infos = self._token_store.get_all_token_info(queries)
            print("DONE QUERIES", datetime.now() - time)
            all_occurrences = reduce(lambda x, y: x & y, [token_dict.keys() for token_dict in all_token_infos.values()])
            print("DONE INTERSECTION", datetime.now() - time)
            all_scores = {page: {'pscore': self._score_position(
                *[all_token_infos[token].get(page).get('all-positions', []) for token in queries]),
                "tscore": sum([all_token_infos[token][page]['tf'] for token in queries]),
                "wscore": sum([all_token_infos[token][page]['weight'] for token in queries])} for
                page in all_occurrences}
            print("DONE SCORING", datetime.now() - time)
            result = list(map(self.convert_http, sorted(all_scores.items(), key=lambda i: (
                i[1]['wscore'] / (1 + math.log(i[1]['pscore'] + 0.00001)), i[1]['tscore']), reverse=True)[:limit]))
            print("DONE SORTING", datetime.now() - time)
            print("DONE SEARCH", datetime.now() - time)
            return result

        else:
            # single word search
            print("SINGLE WORD SEARCH STARTED")
            search_result = self._token_store.path_scores(*queries)
            print("DONE QUERIES WITH SCORING", datetime.now() - time)
            result = list(
                map(self.convert_http,
                    sorted(search_result.items(),
                           key=lambda path_score_pair: path_score_pair[1]["weight"] * math.log10(
                               self.document_count / len(search_result)), reverse=True)[:limit]))

            print("DONE SORTING", datetime.now() - time)
            print("DONE SEARCH", datetime.now() - time)
            return result

    def convert_http(self, path_score_pair: (str, dict)):
        return "{http}{url}".format(http=SearchEngine.HTTP, url=self.book[path_score_pair[0]])
