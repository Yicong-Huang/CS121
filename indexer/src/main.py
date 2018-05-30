import os
import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    store = TokenStore()
    indexer_mode = os.environ.get('INDEXER_MODE', 'SERVER')

    pool = WorkerPool(store, workers=32, book_file=open("WEBPAGES_RAW/bookkeeping.json", 'r'), mode=indexer_mode)

    # capture signal.SIGINT and handle it with safe termination
    signal.signal(signal.SIGINT, lambda signal, frame: pool.safe_terminate())

    pool.execute()
