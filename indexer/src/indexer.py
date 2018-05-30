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
        print(threading.current_thread().getName(), "indexing", path, url)
        token_with_meta = Html(path).get_token_meta()
        if token_with_meta:
            for token, meta in token_with_meta:
                self._token_store.store_page_info(token, path, meta)
            self._token_store.increment_document_count()
        else:
            raise RuntimeError()

    @staticmethod
    def safe_terminate():
        print(threading.current_thread().getName(), "terminated safely")
