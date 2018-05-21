import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    store = TokenStore()

    store.deduplicate()

    pool = WorkerPool(store, workers=24, book_file=open("WEBPAGES_RAW/bookkeeping.json", 'r'))


    def signal_handler(signal, frame):
        pool.safe_terminate()


    signal.signal(signal.SIGINT, signal_handler)
    pool.execute()
