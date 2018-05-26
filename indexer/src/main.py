import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    store = TokenStore()

    store.deduplicate()

    pool = WorkerPool(store, workers=64, book_file=open("WEBPAGES_RAW/bookkeeping.json", 'r'))

    # capture signal.SIGINT and handle it with safe termination
    signal.signal(signal.SIGINT, lambda signal, frame: pool.safe_terminate())

    pool.execute()
