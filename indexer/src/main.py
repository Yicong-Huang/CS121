import os
import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    pool = WorkerPool(TokenStore(), workers=32, book_file=open("../WEBPAGES_RAW/bookkeeping.json", 'r'),
                      mode=os.environ.get('INDEXER_MODE', 'SERVER'))
    # capture signal.SIGINT and handle it with safe termination
    signal.signal(signal.SIGINT, lambda _s, _f: pool.safe_terminate())
    pool.execute()
