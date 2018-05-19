from indexer import Indexer
from poolqueue import PoolQueue
import json
import threading

class WorkerPool:
    def __init__(self, store, workers, bookfile):
        self.workers = workers
        self.bookfile = bookfile
        self.entries = {}
        self.workqueue = PoolQueue()
        self.store = store
        self._setup(store)

    def _setup(self, store):
        with open(self.bookfile, 'r') as file:
            self.entries = json.load(file)
            self.workqueue.enqueue_idles(((k,v) for k,v in self.entries.items()))

    def _worker(self):
        while True:
            item = self.workqueue.get_next_job()
            if item is None:
                break
            Indexer(self.store).index(*item)
            self.workqueue.complete(item)

    def execute(self):
        threads = []
        for _ in range(self.workers):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
