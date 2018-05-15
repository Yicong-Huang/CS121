import re
from collections import Counter

from bs4 import BeautifulSoup


class Html:
    def __init__(self, path, url):
        print("parsing", url, "at path", path)
        self.path = path
        self.url = url
        self.data = ''.join(open("./WEBPAGES_RAW/" + path, encoding="utf-8").readlines()).lower()
        try:
            self.data = BeautifulSoup(self.data, 'xml').get_text()
        except:
            print("not html")

    def tokens(self):
        text = re.findall('[a-zA-Z\d]+', self.data)
        # Get token frequency with collections.Counter object, should be O(n) of time since it will be iterating entire
        # iterator of tokens.
        return Counter(text)
