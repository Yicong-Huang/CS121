class SearchEngine:

    # Todo: add multiple word search support
    # Todo: create search for metadata support
    # Todo: add search based on distance of documents
    def __init__(self, store):
        self._token_store = store

    def search(self, query):
        """
        search is a generator function that yields a sequence of urls that
        matches the query from the user
        """
        for page in (value[0] for value in self._token_store.zrevrange(query)):
            decoded_page = self._token_store.decode(page)
            yield decoded_page

    def show_search(self, queries:list, limit=10):
        """
        show_search method shows the result of one query search
        each result will contains "its number" "url", "tf-idf values"
        """

        print("queryies:", queries, "limit", limit)
        result = []
        try:
            # result =
            for query in queries:
                result = result or result & set(self.search_with_tf_idf(query))

            # for:
            #     t = print(index, result)
            #     if limit and index == limit:
            #         break
            # t
        except:
            print("No Result")
        return result



    def search_with_tf_idf(self, query):
        for page in sorted(self._token_store._redis.zrange(self._token_store.prefixed(query), 0, -1),
                           key=lambda page: self._token_store.tf_idf(query, page), reverse=True):
            yield self._token_store.decode(page)
