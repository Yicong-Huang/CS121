import json
import threading
import time

from indexer import Indexer
from job import Job
from poolqueue import PoolQueue


# Todo: add logging to log workers' activities

class WorkerPool:
    def __init__(self, token_store, workers, book_file, slave=False):
        self._threads = []
        self._workers = workers
        self._book_file = book_file
        self._work_queue = PoolQueue()
        self._token_store = token_store
        self._slave = slave
        self._setup(book_file)
        self._running = True

    def _setup(self, file):
        if self._slave:
            return
        if not self._work_queue.indexer_jobs_completed() and not self._work_queue.get_idle() and not self._work_queue.get_active():
            self._work_queue.enqueue_idles((Job(path, url) for path, url in self._sort_jobs(json.load(file))))

        for _ in self._token_store.get_active():
            self._token_store._redis.rpoplpush(PoolQueue.ACTIVE, PoolQueue.IDLE)

    @staticmethod
    def _sort_jobs(job_dict):
        return sorted(list(job_dict.items()), key=lambda item: tuple(int(i) for i in item[0].split("/")), reverse=True)

    def _worker(self):
        indexer = Indexer(self._token_store)
        while self._running:
            job = self._work_queue.get_next_job()
            if job is None:
                break
            indexer.run(job.path, job.url)
            self._work_queue.complete(job)
        indexer.safe_terminate()

    def execute(self):
        self._threads = []
        for i in range(self._workers):
            t = threading.Thread(target=self._worker)
            t.setName('Worker ' + str(i + 1))
            t.daemon = True
            t.start()
            self._threads.append(t)

        for thread in self._threads:
            thread.join()

    def safe_terminate(self):
        self._running = False

        def check_active():
            while self._work_queue.has_active_job():
                print("Still have active jobs...")
                time.sleep(1)

        active_jobs_checker = threading.Thread(target=check_active)
        active_jobs_checker.daemon = True
        active_jobs_checker.start()
        active_jobs_checker.join()
        print("Terminating now.")
