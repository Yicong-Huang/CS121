import json

from HTML import Html


class Indexer:

    def __init__(self, token_store):
        self.store = token_store

    def run(self, book_file):
        urls = json.load(book_file)
        in_progress_document = self.store.get_in_progress_document()
        last_document = self.store.get_last_document()

        for path, url in list(urls.items())[:100]:
            document = path + ":" + url

            if in_progress_document or last_document:
                if document != in_progress_document:
                    print("skipping", path)
                    continue
                elif document == in_progress_document:
                    print("deleting", path)
                    self.store.delete_in_progress_document()
                    in_progress_document = None
                elif document != last_document:
                    print("skipping", path)
                    continue

            h = Html(path, url)

            self.store.set_in_progress_document(document)
            for token, n in h.tokens().items():
                self.store.store_token(token, document, amount=n)
            self.store.increment_document_count()
            self.store.finish_document()

    def show_store(self):
        print(list(self.store.token_occurrence_pairs()))
