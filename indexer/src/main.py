from indexer import Indexer
from tokenstore import TokenStore
from workerpool import WorkerPool

if __name__ == '__main__':
    store = TokenStore()
    # indexer = Indexer(store)

    store.deduplicate()
    print("Done deduplicating.")

    pool = WorkerPool(store, workers=16, bookfile="WEBPAGES_RAW/bookkeeping.json")
    pool.execute()

    # book_file = open("WEBPAGES_RAW/bookkeeping.json")
    # indexer.run(book_file)
