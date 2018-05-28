import threading

from job import Job
from redisconnection import RedisConnection


class PoolQueue:
    IDLE = 'idle'
    ACTIVE = 'active'

    def __init__(self, token_store=None):
        self._redis = RedisConnection()
        self._token_store = token_store

    def get_idle(self):
        return self._redis.lrange(PoolQueue.IDLE, 0, -1)

    def get_active(self):
        return self._redis.lrange(PoolQueue.ACTIVE, 0, -1)

    def has_idle_job(self):
        return len(self._redis.lrange(PoolQueue.IDLE, 0, 0)) != 0

    def has_active_job(self):
        return len(self._redis.lrange(PoolQueue.ACTIVE, 0, 0)) != 0

    def indexer_jobs_completed(self):
        return self._redis.get("indexer:jobs:completed") == 'True'

    def enqueue_idles(self, jobs, queue=IDLE):
        print("Enqueuing jobs...")
        pipeline = self._redis.pipeline()
        for job in jobs:
            pipeline.rpush(queue, job)
        pipeline.execute()

    def get_next_job(self, f=IDLE, t=ACTIVE):
        job_bytes = self._redis.rpoplpush(f, t)
        if job_bytes is None:
            self._redis.set("indexer:jobs:completed", "True")
            print("No more job available!")
        else:
            job = Job.bytes_to_job(job_bytes)
            print(threading.current_thread().getName(), "get Next Job: %s" % job.path)
            return job

    def complete(self, job, queue=ACTIVE):
        print(threading.current_thread().getName(), "completed Job: %s" % job.path)
        self._redis.lrem(queue, 1, job)
