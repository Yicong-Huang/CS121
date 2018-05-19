import redis

def decode(s):
    return s.decode('utf-8')

class PoolQueue:
    def __init__(self, rhost='127.0.0.1', rport=6379, rdb=0):
        self.redis = redis.Redis(host=rhost, port=rport, db=rdb)

    def enqueue_idle(self, job, queue='idle'):
        self.redis.rpush(queue, job)

    def get_next_job(self, f='idle', t='active'):
        job = self.redis.rpoplpush(f, t)
        print("Get Next Job: %s" % job)
        return decode(job)

    def complete(self, job, queue='active'):
        print("Completed Job: %s" % job)
        self.redis.lrem(queue, job)

    # def deduplicate(self):
