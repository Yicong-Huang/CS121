from redisconnection import RedisConnection


class TokenStore:
    def __init__(self, prefix='t'):
        self._prefix = prefix
        self._redis = RedisConnection()

    def _uglify_meta(self, meta):
        return "/".join(map(str, [meta['weight'], meta['all-positions']]))

    def _unuglify_meta(self, meta_str):
        return dict(zip(['weight', 'all-positions'], meta_str.split('/')))

    def store_page_info(self, token, page, meta):
        """
        token: "myToken"
        page: "0/0"
        meta:
            tf: 20
            weight: 5
            all-positions: [1,2,3]
        """

        meta['all-positions'] = ','.join(map(str, meta['all-positions']))
        meta = self._uglify_meta(meta)
        self._redis.hmset(self.prefixed(token), {page: meta})

    def get_page_info(self, token, page):
        meta = self._unuglify_meta(self._redis.hget(self.prefixed(token), page))

        meta['weight'] = int(meta['weight'])
        meta['all-positions'] = map(int, meta['all-positions'].split(','))
        meta['tf'] = len(meta['all-positions'])
        return meta

    def prefixed(self, token: str) -> str:
        """
        prefix token with the format of self._prefix:token
        :param token: a word from the document
        :return: formatted token string
        """
        return "{}:{}".format(self._prefix, token)

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

    def meta_dict(self, meta_str):
        meta = self._unuglify_meta(meta_str)
        meta['weight'] = int(meta['weight'])
        meta['tf'] = len(meta['all-positions'])
        meta['all-positions'] = map(int, meta['all-positions'].split(','))
        return meta
