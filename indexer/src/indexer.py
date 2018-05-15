from HTML import Html


class indexer:

    def __init__(self, token_store):
        self.ts = token_store
    # @staticmethod
    # def tokenize(html:html):
    #


if __name__ == '__main__':
    # indexer(TokenStore())
    h = Html(open('./test.html'))

    print(h.tokens())
