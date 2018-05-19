import math

import redis


class TokenStore:

    @staticmethod
    def decode(s):
        return s.decode('utf-8')

    def __init__(self, prefix='token'):
        self._prefix = prefix
        self._redis = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def store_token(self, token, page, amount=1):
        if not self._redis.zincrby(self.prefixed(token), page, amount=amount):
            raise RuntimeError("Error: Failed to storeIndex(token: {}, page: {})!".format(token, page))

    def tokens(self):
        return (TokenStore.decode(x) for x in self._redis.scan_iter(self.prefixed("*")))

    def token_occurrence_pairs(self):
        for token in self.tokens():
            yield token, map(lambda x: (TokenStore.decode(x[0]), x[1]),
                             self._redis.zrange(token, 0, -1, withscores=True))

    def prefixed(self, token):
        return "{}:{}".format(self._prefix, token)

    def get_tokens_on_page(self, page):
        return (key for key, val in self.token_occurrence_pairs() if str(page) in map(lambda x: x[0], val))

    def occurrences(self):
        return (pair[1] for pair in self.token_occurrence_pairs())

    def pages_count(self, token):
        return self._redis.zcard(self.prefixed(token))

    def tf(self, token, page):
        return int(self._redis.zscore(self.prefixed(token), page))

    def idf(self, token):
        return math.log(self.get_document_count() / self.pages_count(token))

    def increment_document_count(self):
        self._redis.incr("document_count")

    def get_document_count(self):
        return int(self._redis.get("document_count") or 0)

    def zrevrange(self, token):
        return self._redis.zrevrange(self.prefixed(token), 0, -1, withscores=True)
