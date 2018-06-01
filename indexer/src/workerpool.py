import threading
import time

from indexer import Indexer
from job import Job
from poolqueue import PoolQueue
from redisconnection import RedisConnection


class WorkerPool:
    SERVER_MODE = "SERVER"
    CLIENT_MODE = "CLIENT"

    def __init__(self, token_store, worker_num, bookkeeping: dict, mode):
        self._workers = set()
        self._worker_num = worker_num
        self._redis = RedisConnection.shared().get_connection()
        self._work_queue = PoolQueue()
        self._token_store = token_store
        self._mode = mode
        self._setup(bookkeeping)
        self._running = True
        self._running_thread = None

    def _reenqueue_active(self):
        for _ in self._work_queue.get_active():
            pipeline = self._redis.pipeline()
            pipeline.rpoplpush(PoolQueue.ACTIVE, PoolQueue.IDLE)
            pipeline.execute()

    def _setup(self, bookkeeping):
        if self._mode == WorkerPool.CLIENT_MODE:
            return

        if not any([self._work_queue.indexer_jobs_completed(),
                    self._work_queue.has_idle_job(),
                    self._work_queue.has_active_job()]):
            self._work_queue.enqueue_idles((Job(path, url) for path, url in self._sort_jobs(bookkeeping)))

        self._reenqueue_active()  # move all active jobs to idle on startup

    @staticmethod
    def _sort_jobs(job_dict):
        return sorted(list(job_dict.items()), key=lambda item: tuple(int(i) for i in item[0].split("/")), reverse=True)

    def _execute_client(self):
        def worker():
            indexer = Indexer(self._token_store)
            while self._running:
                job = self._work_queue.get_next_job()
                if job is None:
                    break
                indexer.run(job.path, job.url)
                self._work_queue.complete(job)
            indexer.safe_terminate()

        def listener():
            pubsub = self._redis.pubsub()
            pubsub.subscribe("indexer:clients")
            for message in pubsub.listen():
                if message.get("data") == "TERMINATE":
                    print("!!! RECEIVED TERMINATE FROM SERVER !!!")
                    self.safe_terminate()
                    break

        listener_thread = threading.Thread(target=listener)
        listener_thread.daemon = True
        listener_thread.start()

        for i in range(self._worker_num):
            t = threading.Thread(target=worker, name="Worker-{num}".format(num=i + 1))
            t.start()
            self._workers.add(t)

    def _execute_server(self):
        def server():
            while self._running:
                active_jobs = self._work_queue.get_active()
                idle_jobs = self._work_queue.get_idle()
                clients = self._redis.pubsub_numsub("indexer:clients")[0][1]
                print("Number of active jobs: {}, number of idle jobs: {}, number of clients: {}".format(
                    len(active_jobs), len(idle_jobs), clients))
                if not clients and active_jobs:
                    print("No more clients connected. Re-enqueuing active jobs to idle...")
                    self._reenqueue_active()
                time.sleep(1)

        self._running_thread = threading.Thread(target=server)
        self._running_thread.start()

    def execute(self):
        print("Executing as {mode}".format(mode=self._mode))
        if self._mode == WorkerPool.CLIENT_MODE:
            self._execute_client()
        elif self._mode == WorkerPool.SERVER_MODE:
            self._execute_server()

    def safe_terminate(self):
        self._running = False

        def terminator():
            if self._mode == WorkerPool.SERVER_MODE:
                while True:
                    clients = self._redis.pubsub_numsub("indexer:clients")[0][1]
                    if clients == 0:
                        return
                    self._redis.publish("indexer:clients", "TERMINATE")
                    print("Waiting for {} clients to disconnect...".format(clients))
                    time.sleep(1)
            elif self._mode == WorkerPool.CLIENT_MODE:
                while self._workers:
                    worker = self._workers.pop()
                    worker.join()
                    print("Joined {worker}".format(worker=worker.getName()), "still waiting for {num} workers".format(
                        num=len(self._workers)) if self._workers else "all workers joined")

        terminator_thread = threading.Thread(target=terminator)
        terminator_thread.start()
        terminator_thread.join()

        if self._running_thread:
            self._running_thread.join()

        print("Terminating {mode} now.".format(mode=self._mode))
