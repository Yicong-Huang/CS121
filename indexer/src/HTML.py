
from collections import Counter
import re
from bs4 import BeautifulSoup

class Html:
    def __init__(self, path, url):
        print("parsing", url, "at path", path)
        self.path = path
        self.url = url
        self.data = ''.join(open("./WEBPAGES_RAW/" + path, encoding="utf-8").readlines()).lower()
        self.stop_words = open("stop_words.txt").readline().split(",")
        try:
            self.soup = BeautifulSoup(self.data, 'html.parser')
        
        #print(self.stop_words)
        except:
            print("not html")

    def tokens(self):
        #print(type(self.soup))
        text = ''.join(self.soup.findAll(text = True))
        text = re.sub("[^A-Z0-9a-z<> ]","",text)
        text = re.sub("[<>]","",text)
    

        return Counter([word for word in text.split() if not word in self.stop_words])
        #text = re.findall('[a-zA-Z\d]+', self.data)
        #print(text)
        # Get token frequency with collections.Counter object, should be O(n) of time since it will be iterating entire
        # iterator of tokens.
        #return Counter(text)