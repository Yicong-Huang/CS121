import threading

from HTML import Html


class Indexer:
    # Todo: differentiate html and other files, could build exceptions in HTML

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
        document = path + ":" + url
        print(threading.current_thread().getName(), "indexing", path, url)
        h = Html(path, url)
        for token, n in h.tokens().items():
            self._token_store.store_token(token, document, amount=n)
            self._token_store.increment_document_count()

    @staticmethod
    def safe_terminate():
        print(threading.current_thread().getName(), "terminated safely")
