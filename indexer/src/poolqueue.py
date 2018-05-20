import threading

import redis


def decode(s):
    return s.decode('utf-8')


def encode_job(job):
    return 'job:%s:%s' % job


def decode_job(s):
    s = s.lstrip("job:").split(':')
    parts = (s[0], ''.join(s[1:]))
    print(parts)
    return parts


class PoolQueue:
    IDLE = 'idle'
    ACTIVE = 'active'

    def __init__(self, rhost='127.0.0.1', rport=6379, rdb=0, store=None):
        self.redis = redis.Redis(host=rhost, port=rport, db=rdb)
        self.store = store

    def enqueue_idles(self, jobs, queue=IDLE):
        print("Enqueuing jobs...")
        pipeline = self.redis.pipeline()
        for job in jobs:
            job = encode_job(job)
            pipeline.rpush(queue, job)
        pipeline.execute()

    def get_next_job(self, f=IDLE, t=ACTIVE):
        job = self.redis.rpoplpush(f, t)
        if job is None:
            print("No more job available!")
        else:
            job = decode_job(decode(job))
            print(threading.current_thread().getName(),"get Next Job: %s" % job[0])
        return job

    def complete(self, job, queue=ACTIVE):
        print(threading.current_thread().getName(), "completed Job: %s" % job[0])
        job = encode_job(job)
        self.redis.lrem(queue, job)
