import json
import threading

from indexer import Indexer
from job import Job
from poolqueue import PoolQueue


class WorkerPool:
    def __init__(self, token_store, workers, book_file):
        self._threads = []
        self._workers = workers
        self._book_file = book_file
        self._work_queue = PoolQueue()
        self._token_store = token_store
        self._setup(book_file)

    def _setup(self, file):
        if not self._token_store.get_idle():
            self._work_queue.enqueue_idles((Job(path, url) for path, url in json.load(file).items()))

    def _worker(self):
        indexer = Indexer(self._token_store)
        while True:
            job = self._work_queue.get_next_job()
            if job is None:
                break
            indexer.run(job.path, job.url)
            self._work_queue.complete(job)

    def execute(self):
        self._threads = []
        for _ in range(self._workers):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            self._threads.append(t)

        for thread in self._threads:
            thread.join()
