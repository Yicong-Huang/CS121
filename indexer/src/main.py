import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

import os

if __name__ == '__main__':
    store = TokenStore()
    slave_mode = (os.environ.get('INDEXER_SLAVE_MODE', '') != '')

    pool = WorkerPool(store, workers=64, book_file=open("WEBPAGES_RAW/bookkeeping.json", 'r'), slave=slave_mode)

    # capture signal.SIGINT and handle it with safe termination
    signal.signal(signal.SIGINT, lambda signal, frame: pool.safe_terminate())

    pool.execute()
