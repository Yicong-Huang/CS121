import json
import threading
import time

from indexer import Indexer
from job import Job
from poolqueue import PoolQueue
from redisconnection import RedisConnection


# Todo: add logging to log workers' activities

class WorkerPool:
    def __init__(self, token_store, workers, book_file, mode):
        self._threads = []
        self._workers = workers
        self._book_file = book_file
        self._redis = RedisConnection()
        self._work_queue = PoolQueue()
        self._token_store = token_store
        self._mode = mode
        self._setup(book_file)
        self._running = True

    def _reenqueue_active(self):
        for _ in self._work_queue.get_active():
            self._redis.rpoplpush(PoolQueue.ACTIVE, PoolQueue.IDLE)

    def _setup(self, file):
        if self._mode == 'CLIENT':
            return

        if not any([self._work_queue.indexer_jobs_completed(), self._work_queue.has_idle_job(),
                    self._work_queue.has_active_job()]):
            self._work_queue.enqueue_idles((Job(path, url) for path, url in self._sort_jobs(json.load(file))))

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
            pubsub.subscribe('indexer:clients')
            while self._running:
                for message in pubsub.listen():
                    if message.get('data', '') == 'TERMINATE':
                        print("!!! RECEIVED TERMINATE FROM SERVER !!!")
                        self._running = False

        listener_thread = threading.Thread(target=listener)
        listener_thread.daemon = True
        listener_thread.start()

        for i in range(self._workers):
            t = threading.Thread(target=worker, name='Worker ' + str(i+1))
            t.start()
            self._threads.append(t)

    def _execute_server(self):
        def server():
            while self._running:
                active_jobs = len(self._work_queue.get_active())
                idle_jobs = len(self._work_queue.get_idle())
                clients = self._redis.pubsub_numsub('indexer:clients')[0][1]
                print('Number of active jobs: %d, number of idle jobs: %d, number of clients: %d' % (active_jobs, idle_jobs, clients))
                if clients == 0 and active_jobs:
                    print('No more clients connected. Re-enqueuing active jobs to idle...')
                    self._reenqueue_active()
                time.sleep(1)

        server_thread = threading.Thread(target=server)
        server_thread.start()
        server_thread.join()

    def execute(self):
        print('Executing as ' + self._mode)
        if self._mode == 'CLIENT':
            self._execute_client()
        elif self._mode == 'SERVER':
            self._execute_server()

    def safe_terminate(self):
        self._running = False

        def terminator():
            if self._mode == 'SERVER':
                while True:
                    clients = self._redis.pubsub_numsub('indexer:clients')[0][1]
                    if clients == 0:
                        return
                    self._redis.publish('indexer:clients', 'TERMINATE')
                    print("Waiting for %d clients to disconnect..." % clients)
                    time.sleep(1)
            elif self._mode == 'CLIENT':
                for i, thread in enumerate(self._threads):
                    print("Joined '%s', still waiting for %d workers" % (thread.getName(), self._workers - (i+1)))
                    thread.join()

        terminator_thread = threading.Thread(target=terminator)
        terminator_thread.start()
        terminator_thread.join()

        print("Terminating %s now." % self._mode)
