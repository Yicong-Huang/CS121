import math
from collections import Generator

from job import Job
from poolqueue import PoolQueue
from redisconnection import RedisConnection


class TokenStore:
    def __init__(self, prefix='t'):
        self._prefix = prefix
        self._redis = RedisConnection()

    def _uglify_meta(self, meta):
        return "/".join(map(str, [meta['tf'], meta['weight'], meta['all-positions']]))

    def _unuglify_meta(self, meta_str):

        return dict(zip(['tf', 'weight', 'all-positions'], meta_str.split('/')))

    def store_page_info(self, token, page, meta):
        """
        token: "myToken"
        page: "0/0"
        meta:
            tf: 20
            weight: 5
            all-positions: [1,2,3]
        """
        meta_key = self.prefixed(token)
        meta['all-positions'] = ','.join(map(str, meta['all-positions']))
        meta = self._uglify_meta(meta)
        self._redis.hmset(meta_key, {page: meta})

    def get_page_info(self, token, page):
        meta_key = self.prefixed(token)
        meta = self._redis.hget(meta_key, page)
        meta = self._unuglify_meta(meta)
        int_meta_keys = ['tf', 'weight']
        for int_meta_key in int_meta_keys:
            meta[int_meta_key] = int(meta[int_meta_key])
        meta['all-positions'] = map(int, meta['all-positions'].split(','))
        return meta

    def tokens(self) -> Generator:
        """
        :return: Generator of all tokens saved in the redis
        """
        return (x for x in self._redis.scan_iter(self.prefixed("*")))

    def token_occurrence_pairs(self):
        for token in self.tokens():
            yield token, map(lambda x: (x[0], x[1]),
                             self._redis.zrange(token, 0, -1, withscores=True))

    def prefixed(self, token: str) -> str:
        """
        prefix token with the format of self._prefix:token
        :param token: a word from the document
        :return: formatted token string
        """
        return "{}:{}".format(self._prefix, token)

    def get_tokens_on_page(self, page: str) -> Generator:
        """
        :param page: path + url of the document
        :return: Generator of all tokens of the page saved in the redis
        """
        return (key for key, val in self.token_occurrence_pairs() if str(page) in map(lambda x: x[0], val))

    def occurrences(self) -> Generator:
        return (pair[1] for pair in self.token_occurrence_pairs())

    def pages_count(self, token: str) -> int:
        """
        :param token: a word from the document
        :return:
        """
        return self._redis.zcard(self.prefixed(token))

    def idf(self, token: str) -> float:
        """
        :param token: a word from the document
        :return: idf(inverse document frequency) value of the specific token
        """
        return math.log10(self.get_document_count() / self.pages_count(token))

    def increment_document_count(self) -> None:
        """
        increment the total number of documents stored in the database
        """
        self._redis.incr("document_count")

    def get_document_count(self) -> int:
        """
        :return: the number of the documents stored in the databse
        """
        return int(self._redis.get("document_count") or 0)

    def get_idle(self):
        return self._redis.lrange(PoolQueue.IDLE, 0, -1)

    def get_pages_by_token(self,token)->Generator:
        '''
            return a generator of pages that has the specific token
        '''
        # page_infos = (x for x in self._redis.scan_iter(self.prefixed(token+":*")))
        # return map(lambda x:x.split(":")[-1],page_infos)
        result = {}
        for key,value in self._redis.hgetall(self.prefixed(token)).items():
            result[key] = self.get_page_info(token,key)
        return result
