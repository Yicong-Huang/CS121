import datetime
import json
import math
from collections import defaultdict
from redisconnection import RedisConnection


class SearchEngine:

    # Todo: add search based on distance of documents
    def __init__(self, store):
        self._token_store = store
        self.book = json.load(
            open("WEBPAGES_RAW/bookkeeping.json", 'r'))

    # def search_one_query(self, query):
    #     """
    #     search is a generator function that yields a sequence of paths that
    #     matches the query from the user
    #     """
    #
    #     return self._token_store.get_pages_by_token(query)

    def search_with_tf_idf(self, query):
        for page in sorted(self._token_store._redis.zrange(self._token_store.prefixed(query), 0, -1),
                           key=lambda page: self._token_store.tf_idf(query, page), reverse=True):
            yield self._token_store.decode(page)

    @staticmethod
    def _score_position(first: list, second: list, *args):
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
        
        time = datetime.datetime.now()
        self.document_count = self._token_store.get_document_count()

        if len(queries) > 1:
            print("MULTIPLE WORD SEARCH START")
            pipeline = RedisConnection.shared().getConnection().pipeline()
            for query in queries:
                pipeline.hgetall(self._token_store.prefixed(query))

            print("DONE INITIALIZE PIPELINES")

            all_token_infos = {token: {page: self._token_store.meta_dict(meta) for page, meta in result.items()} for
                             token, result in zip(queries, pipeline.execute())}

            print("DONE QUERIES", datetime.datetime.now() - time)

            all_occurrences = set()

            for token, info in all_token_infos.items():
                page_set = set(info.keys())
                if not all_occurrences:
                    all_occurrences = page_set
                else:
                    all_occurrences &= page_set

                if not all_occurrences:
                    break

            print("DONE INTERSECTION", datetime.datetime.now() - time)

            all_scores = defaultdict(dict)

            for page in all_occurrences:
                all_positions = []
                tf, weight = 0, 0
                for token in queries:
                    all_positions.append(all_token_infos[token].get(page).get('all-positions', []))
                    tf += all_token_infos[token][page]['tf']
                    weight += all_token_infos[token][page]['weight']
                all_scores[page] = {'pscore': self._score_position(*all_positions), "tscore": tf, "wscore": weight}

            print("DONE SCORING", datetime.datetime.now() - time)

            result = list(map(lambda x: "http://" + self.book[x[0]], sorted(all_scores.items(), key=lambda i: (
                i[1]['wscore'] / (1 + math.log(i[1]['pscore'] + 0.00001)), i[1]['tscore']), reverse=True)[:limit]))

            print("DONE SORTING", datetime.datetime.now() - time)
            return result

        elif len(queries) == 1:
            #single word search

            print("SINGLE WORD SEARCH STARTED")
            search_result = RedisConnection.shared().getConnection().hgetall(self._token_store.prefixed(queries[0]))
        
            for page,meta in search_result.items():
                search_result[page] = self._token_store.meta_dict(meta)
            
            first_ten = list(map(lambda x:"http://"+self.book[x],[key[0] for key in sorted(search_result.items(), key = lambda pair : pair[1]['weight'] * math.log10(self.document_count/len(search_result)), reverse=True)[:10]]))
            return first_ten
        else:
            return ["No input"]
            
