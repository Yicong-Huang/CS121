import json
import threading

from indexer import Indexer
from job import Job
from poolqueue import PoolQueue


class WorkerPool:
    def __init__(self, token_store, workers, book_file):
        self.workers = workers
        self.book_file = book_file
        self.work_queue = PoolQueue()
        self.token_store = token_store
        self._setup(book_file)

    def _setup(self, file):
        if not self.token_store.get_idle():
            self.work_queue.enqueue_idles((Job(path, url) for path, url in json.load(file).items()))

    def _worker(self):
        indexer = Indexer(self.token_store)
        while True:
            job = self.work_queue.get_next_job()
            if job is None:
                break
            indexer.run(job.path, job.url)
            self.work_queue.complete(job)

    def execute(self):
        threads = []
        for _ in range(self.workers):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
