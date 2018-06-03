import json
import os
import signal

from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    bookkeeping = json.load(open("../WEBPAGES_RAW/bookkeeping.json", 'r'))
    store = TokenStore()
    store.store_bookkeeping(bookkeeping)
    pool = WorkerPool(TokenStore(), worker_num=32, bookkeeping=bookkeeping,
                      mode=os.environ.get("INDEXER_MODE", "SERVER"))
    # capture signal.SIGINT and handle it with safe termination
    signal.signal(signal.SIGINT, lambda _s, _f: pool.safe_terminate())
    pool.execute()
