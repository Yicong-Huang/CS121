import threading

from HTML import Html


class Indexer:

    def __init__(self, token_store):
        self.store = token_store

    def run(self, path, url):
        document = path + ":" + url
        print(threading.current_thread().getName(), "indexing", path, url)
        h = Html(path, url)
        for token, n in h.tokens().items():
            self.store.store_token(token, document, amount=n)
        self.store.increment_document_count()
