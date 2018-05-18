from indexer import Indexer
from tokenstore import TokenStore
from search_engine import Search_Engine

def command_line():
    command_line = input("Please type in what do you want to search: ")
    return command_line


if __name__ == '__main__':
    store = TokenStore()
    indexer = Indexer(store)

    book_file = open("WEBPAGES_RAW/bookkeeping.json")
    indexer.run(book_file)
    indexer.show_store()

    search_engine = Search_Engine(store)
    search_query = command_line()
    search_engine.do_search(search_query)
    search_engine.do_show_result(10)
