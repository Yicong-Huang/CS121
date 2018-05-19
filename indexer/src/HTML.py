import re
from collections import Counter

from bs4 import BeautifulSoup


class Html:
    def __init__(self, path, url):

        self.path = path
        self.url = url
        self.data = ''.join(open("./WEBPAGES_RAW/" + path, encoding="utf-8").readlines()).lower()
        try:
            self.soup = BeautifulSoup(self.data, 'html.parser')
        except:
            print("not html")

    def tokens(self):

        return Counter(re.findall("[a-zA-Z\d]+", self.soup.get_text()))
