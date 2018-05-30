import ast

from redisconnection import RedisConnection


class TokenStore:
    def __init__(self, prefix='t'):
        self._prefix = prefix
        self._redis = RedisConnection.shared().get_connection()

    @staticmethod
    def _uglify_meta(meta: dict) -> str:
        """
        transform the meta dictionary into a shortened string to save database usage
        :param meta: a dictionary contains weight score and all positions of the token
        :return: meta_str
        """
        return "{weight}/{positions}".format(weight=meta['weight'], positions=','.join(map(str, meta['all-positions'])))

    @staticmethod
    def _unuglify_meta(meta_str: str) -> dict:
        """
        transform the meta_str get from database back to the meta dictionary
        :param meta_str: a shortened string of meta
        :return: {"tf": int, "weight":int, "all-positions":[int]}
        """
        meta = dict(zip(['weight', 'all-positions'], meta_str.split('/')))
        return {"weight": int(meta['weight']),
                "tf": len(meta['all-positions'].split(',')),
                "all-positions": list(map(int, meta['all-positions'].split(',')))}

    def get_bookkeeping(self):
        return ast.literal_eval(self._redis.get('file:bookkeeping.json'))

    def store_page_info(self, token: str, page: str, meta) -> None:
        """
        store the token-page's meta dictionary into redis
        :param token: a word from the document
        :param page: page path like "0/1"
        :param meta:
        """
        self._redis.hmset(self.prefixed(token), {page: self._uglify_meta(meta)})

    def get_page_info(self, token: str, page: str) -> dict:
        return self._unuglify_meta(self._redis.hget(self.prefixed(token), page))

    def prefixed(self, token: str) -> str:
        """
        prefix token with the format of self._prefix:token
        :param token: a word from the document
        :return: formatted token string
        """
        return "{prefix}:{token}".format(prefix=self._prefix, token=token)

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

    def get_all_token_info(self, tokens: [str]):
        pipeline = self._redis.pipeline()
        for token in tokens:
            pipeline.hgetall(self.prefixed(token))

        return {token: {page: self._unuglify_meta(meta) for page, meta in result.items()}
                for token, result in zip(tokens, pipeline.execute())}

    def path_scores(self, token: str):
        return {path: self._unuglify_meta(meta_str) for path, meta_str in
                self._redis.hgetall(self.prefixed(token)).items()}
