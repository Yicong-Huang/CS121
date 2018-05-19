from indexer import Indexer
from tokenstore import TokenStore

if __name__ == '__main__':
    store = TokenStore()
    indexer = Indexer(store)

    book_file = open("WEBPAGES_RAW/bookkeeping.json")
    indexer.run(book_file)
