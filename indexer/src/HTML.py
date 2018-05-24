from collections import Counter
import re
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
            self._is_html = True
            self.soup = BeautifulSoup(self.data,'html.parser')
        except:
            self._is_html = False
            print('not html')

    '''
    Type of file can be parsed by Html
    html        pass
    txt         pass
    makefile    pass

    jpg         nopass
    '''

    def tokens(self):
        """
        This method will filter out unrelated data in a html file and return a Counter
        of the tokens and the occurrence of tokens in the html file
        """

        if self._is_html:
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

            
            # print(re.findall("[a-zA-Z\d]+", self.soup.get_text(strip=True)))
            temp = ' '.join(self.soup.get_text().split())
            #print(re.findall("[a-zA-Z\d]+",temp))
            return Counter(re.findall("[a-zA-Z\d]+", temp))
        else:
            return Counter()