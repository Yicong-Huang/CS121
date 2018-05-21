import re

from searchengine import SearchEngine
from tokenstore import TokenStore


def command_line(arg=None):
    query = input("Please type in what do you want to search: ").lower()

    if " --" in query and not arg:
        query, arg = query.split(" --")

    query = re.sub("[^A-Za-z0-9]+", "", query)
    valid = False
    while not valid:
        if len(query) > 32:
            print("the query is too long, please shorten the search word")
            query = input("Please type in what do you want to search: ").lower()
            if " --" in query and not arg:
                query, arg = query.split(" --")
            query = re.sub("[^A-Za-z0-9]+", "", query)
        else:
            valid = True
    return query, arg


if __name__ == '__main__':
    store = TokenStore()
    search_engine = SearchEngine(store)
    print("Total number of document parsed: ",search_engine._token_store.get_document_count())
    print("The number of unique tokens: ",search_engine._token_store._redis.dbsize())
    while True:
        search_query, arg = command_line()
        search_engine.show_search(*[search_query, False] if arg == "all" else [search_query])
