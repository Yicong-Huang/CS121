import os

from redis import StrictRedis, ConnectionPool


class RedisConnection:
    __instance = None

    @staticmethod
    def shared():
        if not RedisConnection.__instance:
            RedisConnection()
        return RedisConnection.__instance

    def __init__(self):
        host = os.getenv('INDEXER_REDIS_HOST', '')
        host = host if len(host) > 0 else '127.0.0.1'
        port = os.getenv('INDEXER_REDIS_PORT', '')
        port = int(port) if len(port) > 0 else 6379
        self.pool = ConnectionPool(host=host, port=port, db=0, decode_responses=True)

        if RedisConnection.__instance:
            raise Exception("This class is a singleton!")
        else:
            RedisConnection.__instance = self

    def get_connection(self):
        return StrictRedis(connection_pool=self.pool)
