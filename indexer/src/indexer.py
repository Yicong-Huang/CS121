import json

from HTML import Html


class Indexer:

    def __init__(self, token_store):
        self.store = token_store

    def run(self, book_file):
        urls = json.load(book_file)
        for path, url in list(urls.items())[:10]:
            h = Html(path, url)
            for token, n in h.tokens().items():
                self.store.store_token(token, path + ":" + url, amount=n)
            self.store.increment_document_count()

    def show_store(self):
        print(list(self.store.token_occurrence_pairs()))
