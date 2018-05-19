from indexer import Indexer
from searchengine import SearchEngine
from tokenstore import TokenStore


def command_line():
    return input("Please type in what do you want to search: ")


if __name__ == '__main__':
    store = TokenStore()
    indexer = Indexer(store)

    book_file = open("WEBPAGES_RAW/bookkeeping.json")
    indexer.run(book_file)

    search_engine = SearchEngine(store)
    search_query = command_line()

    search_engine.show_search(search_query)
