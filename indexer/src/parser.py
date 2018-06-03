import re
from collections import defaultdict, Generator

import bs4
import chardet


class Parser:
    """
    a Parser to parse html files, a path like "0/0" will be required
    """

    def __init__(self, path: str):
        text = open("../WEBPAGES_RAW/" + path, encoding="utf-8", mode="r").read()
        # ignore and set self.soup with an empty string if it is an unknown bytes file
        self.soup = bs4.BeautifulSoup(
            text.lower() if chardet.detect(bytearray(text, encoding="utf-8"))['encoding'] else "",
            'html.parser')

    def get_token_meta(self) -> Generator:
        """
        This method will filter out unrelated data in a html file and return a Counter
        of the tokens and the occurrence of tokens in the html file
        """
        positions = defaultdict(list)
        weights = defaultdict(int)

        self._parse_title_weight(weights)
        self._parse_headers_weight(weights)

        for comment in self.soup.findAll(text=lambda text: isinstance(text, bs4.Comment)):
            comment.extract()

        for node_name in ("script", "link", "style"):
            self._extract_node_by_name(node_name)

        tokens = self._find_all_tokens()

        self._score_tokens(tokens, positions, weights)

        for token in set(tokens):
            yield token, {'weight': weights[token], 'all-positions': positions[token]}

    def _score_tokens(self, tokens: [str], positions: {str: [int]}, weights: {str: int}) -> None:
        """
        for each token in the tokens list, record its position and increment weight
        :param tokens: list of tokens
        :param positions: positions of tokens, each position is record in a list, so order maintained
        :param weights: weights of tokens
        """
        for i, token in enumerate(tokens):
            positions[token].append(i)
            self._increment_token_weight(weights, token=token)

    def _find_all_tokens(self) -> [str]:
        """
        find all text nodes and choose the ones that is a word
        :return: a list of tokens
        """
        return re.findall("[a-zA-Z\d]+", self.soup.get_text(separator=" ", strip=True))

    def _extract_node_by_name(self, node_name: str) -> None:
        """
        extract the node with html tag name
        :param node_name: a html tag
        """
        for node in self.soup(node_name):
            node.extract()

    def _parse_title_weight(self, weights: {str: int}) -> None:
        """
        give an extra weight of 4 for tokens in title
        :param weights: weights of tokens
        """
        self._increment_token_weight(weights, tag="title", weight=4)

    def _parse_headers_weight(self, weights: {str: int}) -> None:
        """
        give an extra weight of 2 for tokens in h1 - h6
        :param weights: weights of tokens
        """
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            self._increment_token_weight(weights, tag=tag, weight=2)

    def _increment_token_weight(self, weights: {str: int}, token=None, tag=None, weight=1) -> None:
        """
        give a weight for given token or all tokens in the given tag text
        :param weights: weights of tokens
        :param token: a specific token to increment
        :param tag: a html tag, all tokens in the tag text to increment
        :param weight: the weight to increment each time, 1 by default
        """
        if tag:
            for node in self.soup.find_all(tag):
                for token in re.findall("[a-zA-Z\d]+", node.get_text()):
                    weights[token] += weight
        elif token:
            weights[token] += weight
