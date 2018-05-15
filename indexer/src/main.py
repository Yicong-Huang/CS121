import json

from HTML import Html
from tokenstore import TokenStore

if __name__ == '__main__':
    store = TokenStore()

    urls = json.load(open("WEBPAGES_RAW/bookkeeping.json"))
    for path, url in list(urls.items()):

        h = Html(path, url)
        for token, n in h.tokens().items():
            for _ in range(n):
                # print("pushing", token, "with", path + ":" + url)
                store.store_token(token, path + ":" + url)

    print(list(store.get_tokens_on_page("0/1:www.ics.uci.edu/~ejw/pres/stc-99/sld009.htm")))
