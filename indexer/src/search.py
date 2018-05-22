import re
import signal

from searchengine import SearchEngine
from tokenstore import TokenStore


def command_line(arg=None):
    while True:
        raw_query = input("Please type in what do you want to search: ").lower()

        if " --" in raw_query and not arg:
            raw_query, arg = raw_query.split(" --")

        query = re.sub("[^a-z0-9]+", "", raw_query)

        if len(query) > 32:
            print("the query is too long, please shorten the search word")
        else:
            return query, arg


if __name__ == '__main__':
    store = TokenStore()
    search_engine = SearchEngine(store)

    signal.signal(signal.SIGINT, lambda signal, frame: exit(0))

    while True:
        search_query, arg = command_line()
        search_engine.show_search(*[search_query, False] if arg == "all" else [search_query])
