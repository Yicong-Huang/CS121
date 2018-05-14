import operator
from collections import Counter
from functools import reduce

import redis


def decode(str):
    return str.decode('utf-8')


class TokenStore:
    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def store_token(self, token, page, prefix='token'):
        if self.r.zincrby('%s:%s' % (prefix, token), page) is False:
            raise RuntimeError('Error: Failed to storeIndex(token: %s, page: %s)!', token, page)

    def tokens(self, prefix='token'):
        return (decode(x) for x in self.r.scan_iter('%s:*' % prefix))

    def token_occurrence_pairs(self):
        for token in self.tokens():
            occurrence = self.r.zrange(token, 0, -1, withscores=True)
            yield (token, map(lambda x: (decode(x[0]), x[1]), occurrence))

    def get_tokens_on_page(self, page):
        return (key for key, val in self.token_occurrence_pairs() if str(page) in map(lambda x: x[0], val))

    def occurrences(self):
        return (pair[1] for pair in self.token_occurrence_pairs())

    def pages_count(self):
        return reduce(operator.add, (Counter(x) for x in self.occurrences()))

    def tf(self, token, page):
        for pair in self.r.zrange(token, 0, -1, withscores=True):
            if decode(pair[0]) == str(page):
                return pair[1]
        return 0

    def idf(self, token, page):
        print(list(self.pages_count()))
        pass
