from indexer import Indexer
import json
import queue
import threading

class WorkerPool:
    def __init__(self, store, workers, bookfile):
        self.workers = workers
        self.bookfile = bookfile
        self.entries = {}
        self.workqueue = queue.Queue()
        self.store = store
        self._setup(store)

    def _setup(self, store):
        with open(self.bookfile, 'r') as file:
            self.entries = json.load(file)
            for (k,v) in self.entries.items():
                self.workqueue.put((k,v))

    def _worker(self):
        while True:
            item = self.workqueue.get()
            if item is None:
                break
            Indexer(self.store).parse(*item)

    def execute(self):
        threads = []
        for _ in range(self.workers):
            t = threading.Thread(target=self._worker)
            t.start()
            threads.append(t)

        self.workqueue.join()
