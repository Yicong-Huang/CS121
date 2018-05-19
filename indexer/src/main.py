from parser import Parser
from tokenstore import TokenStore

if __name__ == '__main__':
    store = TokenStore()
    parser = Parser(store)

    book_file = open("WEBPAGES_RAW/bookkeeping.json")
    parser.run(book_file)
