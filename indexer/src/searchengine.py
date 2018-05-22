class SearchEngine:
    def __init__(self, store):
        self._token_store = store

    def search(self, query):
        """
        search is a generator function that yields a sequence of urls that
        matches the query from the user
        """
        for page in (value[0] for value in self._token_store.zrevrange(query)):
            decoded_page = self._token_store.decode(page)
            # yield decoded_page[decoded_page.index(":") + 1:]
            yield decoded_page

    def show_search(self, query, limit=10):
        """
        show_search method shows the result of one query search
        each result will contains "its number" "url", "tf-idf values"
        """
        try:
            for index, result in enumerate(self.search(query), 1):
                # string = ""
                # docID = result[:result.index(":")]
                # tf = 0
                # idf = 0
                # # print(result)
                # tf = self._token_store.tf(query, result)
                # idf = self._token_store.idf(query)
                # string += " TF: "
                # string += str(tf)
                # string += " IDF: "
                # string += str(round(idf, 2))
                # string += " TF-IDF: "
                # # sth = list(self._token_store.get_tokens_on_page(result))
                # # print(sth)
                # # print(string)
                # string += str(round((1 + math.log10(tf)) * idf), 2)
                # string += " "
                t = print(index, result)
                if limit and index == limit:
                    break
            t
        except:
            print("No Result")
