import re
from collections import Counter

from bs4 import BeautifulSoup, Comment


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

        for comment in self.soup.findAll(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        for script in self.soup('script'):
            script.extract()
        for link in self.soup('link'):
            link.extract()
        for style in self.soup("style"):
            style.extract()

        return Counter(re.findall("[a-zA-Z\d]+", self.soup.get_text(strip=True)))
