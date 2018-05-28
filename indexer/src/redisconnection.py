import os
from redis import StrictRedis

def RedisConnection():
    host = os.getenv('INDEXER_REDIS_HOST', '')
    host = host if len(host) > 0 else '127.0.0.1'
    port = os.getenv('INDEXER_REDIS_PORT', '')
    port = int(port) if len(port) > 0 else 6379
    return StrictRedis(host=host, port=port, db=0, decode_responses=True)
