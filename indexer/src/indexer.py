import json

from HTML import Html


class Indexer:

    def __init__(self, token_store):
        self.store = token_store

    def run(self, book_file):
        urls = json.load(book_file)
        in_progress_document = self.store.get_in_progress_document()
        last_document = self.store.get_last_document()

        for path, url in urls.items():
            document = path + ":" + url

            if in_progress_document or last_document:
                if (in_progress_document and document != in_progress_document) or (
                        last_document and document != last_document):
                    continue
                elif document == in_progress_document:
                    print("restart with", path)
                    print("deleting unfinished", path)
                    self.store.delete_in_progress_document()
                    in_progress_document = None

                elif document == last_document:
                    last_document = None
                    continue

            h = Html(path, url)

            self.store.set_in_progress_document(document)
            for token, n in h.tokens().items():
                self.store.store_token(token, document, amount=n)
            self.store.increment_document_count()
            self.store.finish_document()

    def show_store(self):
        print(list(self.store.token_occurrence_pairs()))
