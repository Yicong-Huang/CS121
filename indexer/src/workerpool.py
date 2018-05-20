import json
import threading

from indexer import Indexer
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
            self.work_queue.enqueue_idles(json.load(file).items())

    def _worker(self):
        indexer = Indexer(self.token_store)
        while True:
            item = self.work_queue.get_next_job()
            if item is None:
                break
            indexer.index(*item)
            self.work_queue.complete(item)

    def execute(self):
        threads = []
        for _ in range(self.workers):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
