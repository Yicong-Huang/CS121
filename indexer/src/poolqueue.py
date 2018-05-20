import threading

import redis

from job import Job


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
            pipeline.rpush(queue, job)
        pipeline.execute()

    def get_next_job(self, f=IDLE, t=ACTIVE):
        job_bytes = self.redis.rpoplpush(f, t)
        if job_bytes is None:
            print("No more job available!")
        else:
            job = Job.bytes_to_job(job_bytes)
            print(threading.current_thread().getName(), "get Next Job: %s" % job.path)
            return job

    def complete(self, job, queue=ACTIVE):
        print(threading.current_thread().getName(), "completed Job: %s" % job.path)
        self.redis.lrem(queue, job)
