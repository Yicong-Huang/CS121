import re
from collections import Counter

from bs4 import BeautifulSoup, Comment


class Html:
    """
    This class is a Parser to parse HTML files, a path like "0/0" and a url like "https://..."
    will be required as parameters in __init__ method
    """

    def __init__(self, path, url):

        self.path = path
        self.url = url
        self.data = ''.join(open("./WEBPAGES_RAW/" + path, encoding="utf-8").readlines()).lower()
        try:
            self.soup = BeautifulSoup(self.data, 'html.parser')
        except:
            print("not html")

    def tokens(self):
        """
        This method will filter out unrelated data in a html file and return a Counter
        of the tokens and the occurrence of tokens in the html file
        """
        for comment in self.soup.findAll(text=lambda text: isinstance(text, Comment)):
            comment.extract()

        # strip off the content surrounded by <script>
        for script in self.soup('script'):
            script.extract()

        # strip off the content surrounded by <link>
        for link in self.soup('link'):
            link.extract()

        # strip off the CSS style, which is surrounded by <style>
        for style in self.soup("style"):
            style.extract()

        return Counter(re.findall("[a-zA-Z\d]+", self.soup.get_text(strip=True)))
