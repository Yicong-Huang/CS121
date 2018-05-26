import re
from collections import Counter, defaultdict

from bs4 import BeautifulSoup, Comment


class Html:
    """
    This class is a Parser to parse HTML files, a path like "0/0" and a url like "https://..."
    will be required as parameters in __init__ method
    """

    def __init__(self, path, url):

        """
        Type of file can be parsed by Html
        html        pass
        txt         pass
        makefile    pass

        jpg         nopass
        """

        self.path = path
        self.url = url

        self.data = ''.join(open("./WEBPAGES_RAW/" + path, encoding="utf-8").readlines()).lower()
        # self.data = ''.join(open("./test.html", encoding="utf-8").readlines()).lower()
        try:
            self._is_html = True
            self.soup = BeautifulSoup(self.data, 'html.parser')
        except:
            self._is_html = False
            print('not html')

    def token_metas(self):
        """
        This method will filter out unrelated data in a html file and return a Counter
        of the tokens and the occurrence of tokens in the html file
        """
        positions = defaultdict(list)
        weights = defaultdict(int)

        if self._is_html:

            self.parse_title(weights)
            self.parse_headers(weights)

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
            tokens = ' '.join(self.soup.get_text().split())
            tokens = re.findall("[a-zA-Z\d]+", tokens)

            for i, token in enumerate(tokens):
                positions[token].append(i)
                self._increment_token_weight(weights, token=token)
            print(tokens)
            print(positions, len(positions))
            print(weights, len(weights))
            tfs = Counter(tokens)
            for token, tf in tfs.items():
                print(token, tf)
                yield (token, {'tf': tf, 'weight': weights[token], 'all-positions': positions[token]})

    def parse_title(self, _weight_dict: dict):
        self._increment_token_weight(_weight_dict, tag="title", weight=4)

    def parse_headers(self, _weight_dict: dict):
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self._increment_token_weight(_weight_dict, tag=tag, weight=2)

    def _increment_token_weight(self, _weight_dict: dict, token=None, tag=None, weight=1):
        if tag:
            for node in self.soup.find_all(tag):
                for token in re.findall("[a-zA-Z\d]+", node.get_text()):
                    _weight_dict[token] += weight
        elif token:
            _weight_dict[token] += weight
        else:
            raise RuntimeError("no token or tag specified")


if __name__ == '__main__':
    h = Html('0/2', "fano.ics.uci.edu/cites/Author/Murray-Sherk.html")
    print(list(h.token_metas()))
