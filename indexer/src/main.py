from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    store = TokenStore()

    store.deduplicate()
    print("Done deduplicating.")

    pool = WorkerPool(store, workers=24, book_file=open("WEBPAGES_RAW/bookkeeping.json", 'r'))
    pool.execute()
