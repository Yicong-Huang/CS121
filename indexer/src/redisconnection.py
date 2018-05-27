import os
from redis import Redis

def RedisConnection():
    host = os.environ.get('INDEXER_REDIS_HOST', '127.0.0.1')
    port = int(os.environ.get('INDEXER_REDIS_PORT', 6379))
    return Redis(host=host, port=port, db=0, decode_responses=True)
