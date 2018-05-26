import math
from collections import Generator

from redis import Redis

from job import Job
from poolqueue import PoolQueue


class TokenStore:
    def __init__(self, prefix='token'):
        self._prefix = prefix
        self._redis = Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        self._meta_transform = {'tf': 't', 'weight': 'w', 'all-positions': 'a'}

    def _uglify_meta(self, meta):
        for fm, to in self._meta_transform.items():
            meta[to] = meta.pop(fm)

    def _unuglify_meta(self, meta):
        for fm, to in self._meta_transform.items():
            meta[fm] = meta.pop(to)

    def store_page_info(self, token, page, meta):
        """
        token: "myToken"
        page: "0/0"
        meta:
            tf: 20
            weight: 5
            all-positions: [1,2,3]
        """
        meta_key = self.prefixed('%s:%s' % (token, page))
        meta['all-positions'] = ','.join(map(str, meta['all-positions']))
        self._uglify_meta(meta)
        self._redis.hmset(meta_key, meta)

    def get_page_info(self, token, page):
        meta_key = self.prefixed('%s:%s' % (token, page))
        meta = self._redis.hgetall(meta_key)
        self._unuglify_meta(meta)
        int_meta_keys = ['tf', 'weight']
        for int_meta_key in int_meta_keys:
            meta[int_meta_key] = int(meta[int_meta_key])
        meta['all-positions'] = list(map(int, meta['all-positions'].split(',')))
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

    def tf(self, token: str, page: str) -> float:
        """
        :param token: a word from the document
        :param page: path + url of the document
        :return: tf value(term frequency) of the specific token in the specific document
        """
        return int(self._redis.zscore(self.prefixed(token), page))

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

    def zrevrange(self, token: str) -> list:
        """
        :param token: a word from the document
        :return: a list of urls contains the specific token and sorted by the token's occurenece
        """
        return self._redis.zrevrange(self.prefixed(token), 0, -1, withscores=True)

    def deduplicate(self) -> None:
        """
        delete unfinished documents from _redis to prevent duplications.
        :return: None
        """
        print("Searching for unfinished jobs...")
        active_jobs = list(map(Job.bytes_to_job, self._redis.lrange(PoolQueue.ACTIVE, 0, -1)))
        if not active_jobs:
            print("No unfinished jobs!")
            return
        pipeline = self._redis.pipeline()
        self.delete_pages((job.path for job in active_jobs), pipeline)

        for _ in active_jobs:
            self._redis.rpoplpush(PoolQueue.ACTIVE, PoolQueue.IDLE)
        self._redis.delete(PoolQueue.ACTIVE)
        pipeline.execute()
        print("Done deduplicating.")

    def delete_pages(self, pages: Generator, pipeline):
        """
        delete unfinished pages
        :param pages:
        :param pipeline:
        :return:
        """

        for token in self.tokens():
            for page in pages:
                print("deleting", page)
                pipeline.zrem(token, page)

    def get_idle(self):
        return self._redis.lrange(PoolQueue.IDLE, 0, -1)