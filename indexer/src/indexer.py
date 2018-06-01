import itertools
import threading
from collections import Iterator

from parser import Parser


def peek(iterable) -> (bool, Iterator):
    try:
        first = next(iterable)
    except StopIteration:
        return False, None
    return True, itertools.chain([first], iterable)


class Indexer:
    def __init__(self, token_store):
        self._token_store = token_store

    def run(self, path: str, url: str) -> None:
        """
        run the indexer, create a HTML instance to parse the document, and push all tokens with it's frequency in the
        document into _token_store
        :param path: document path in WEBPAGES_RAW
        :param url: corresponding url for the document
        :return: None
        """
        print(threading.current_thread().getName(), "indexing", path, url)
        has_token, token_with_meta = peek(Parser(path).get_token_meta())
        if has_token:
            for token, meta in token_with_meta:
                self._token_store.store_page_info(token, path, meta)
            self._token_store.increment_document_count()

    @staticmethod
    def safe_terminate():
        print(threading.current_thread().getName(), "terminated safely")
