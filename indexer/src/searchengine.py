class SearchEngine:
    def __init__(self, store):
        self._token_store = store

    def search(self, query):
        for page in (value[0] for value in self._token_store.zrevrange(query)):
            decoded_page = self._token_store.decode(page)
            yield decoded_page[decoded_page.index(":") + 1:]

    def show_search(self, query):

        try:
            for index, result in enumerate(self.search(query), 1):
                t = print(index, result)
            t
        except:
            print("No Result")
