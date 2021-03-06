import logging
import re
from collections import defaultdict, OrderedDict
from itertools import imap, ifilter
from time import time
from urlparse import urlparse

from lxml import html

from datamodel.search.Yicongh1ZicanlHwo_datamodel import Yicongh1ZicanlHwoLink, OneYicongh1ZicanlHwoUnProcessedLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"


@Producer(Yicongh1ZicanlHwoLink)
@GetterSetter(OneYicongh1ZicanlHwoUnProcessedLink)
class CrawlerFrame(IApplication):
    app_id = "Yicongh1ZicanlHwo"

    starttime = time()

    def __init__(self, frame):
        self.app_id = "Yicongh1ZicanlHwo"
        self.frame = frame
        self.visit_counts = defaultdict(int)
        self.pattern_counts = defaultdict(int)
        self.outlink_counts = defaultdict(int)
        self.download_counts = defaultdict(int)
        self.total_download_counts = 0
        self.query_counts = defaultdict(int)

    def initialize(self):
        self.count = 0
        links = self.frame.get_new(OneYicongh1ZicanlHwoUnProcessedLink)
        if len(links) > 0:
            print "Resuming from the previous state."
            self.download_links(links)
        else:
            l = Yicongh1ZicanlHwoLink("http://www.ics.uci.edu/")
            print l.full_url
            self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get_new(OneYicongh1ZicanlHwoUnProcessedLink)
        if unprocessed_links:
            self.download_links(unprocessed_links)

    def download_links(self, unprocessed_links):
        if shouldShutdown(self.total_download_counts):
            self.done = True

        for link in unprocessed_links:
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            self.total_download_counts += 1
            links = extract_next_links(downloaded, self.visit_counts, self.pattern_counts, self.outlink_counts, self.download_counts, self.query_counts)
            for l in links:
                if is_valid(l):
                    self.frame.add(Yicongh1ZicanlHwoLink(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")

        # Subdomains
        # print Counter([subdomain(x) for x in self.download_counts.keys()]).items()

        # Outlinks
        key = max(self.outlink_counts, key=self.outlink_counts.get)
        print(key, self.outlink_counts[key])

        # print (self.visit_counts, self.outlink_counts)


def removeFragment(url):
    return url.split("#")[0]


def removeQuery(url):
    return url.split("?")[0]


def isNotAsset(url):
    return not isAsset(url)


def isHttpOrHttps(url):
    return any(url.startswith(x + "://") for x in ["http", "https"])


def subdomain(url):
    return urlparse(url).hostname.split('.')[0]


def isInDomain(domain):
    def validator(url):
        return domain in urlparse(url).hostname

    return validator


def isAsset(url):
    url = removeFragment(removeQuery(url))
    return re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                    + "|thmx|mso|arff|rtf|jar|csv" \
                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", url)


def linkCount(f, visit_counts):
    def counter(url):
        should_return = f(visit_counts[url])
        if should_return:
            visit_counts[url] += 1
        return should_return

    return counter


def patternCount(lookup, pattern_counts):
    def counter(url):
        for entry in lookup:
            if re.search(entry, url) is not None:
                pattern_counts[entry] += 1
                return pattern_counts[entry] <= lookup[entry] or lookup[entry] == -1
        raise KeyError("Cannot find pattern for %s" % url)

    return counter


def applyFilters(filters, iterable):
    return reduce(lambda s, f: ifilter(f, s), filters, iterable)


def shouldShutdown(total_download_counts):
    return total_download_counts > 5000



def queryCount(num_limit,query_counts):
    def count(url):
        url = url.split("?")[0]
        result = query_counts[url] < num_limit
        if result:
            query_counts[url] += 1
        return result
    return count

def stripTrailingSlash(url):
  return url.strip('/')

def imap_multiple(iterable, function, *f):
  if f:
    return imap_multiple(imap(function, iterable), *f)
  return imap(function, iterable)

def extract_next_links(rawDataObj, visit_counts, pattern_counts, outlink_counts, download_counts,query_counts):
    outputLinks = []
    print rawDataObj.url.encode("utf-8")
    rawDataObj.url = rawDataObj.url.encode("utf-8")
    rawDataObj.url = stripTrailingSlash(rawDataObj.url)
    try:
        doc = html.document_fromstring(rawDataObj.content)
        doc.make_links_absolute(
            rawDataObj.final_url.encode("utf-8") if rawDataObj.is_redirected else rawDataObj.url.encode("utf-8"))

        urls = [i[2].encode("utf-8") for i in doc.iterlinks()]

        # Count the number of outlinks on the page
        outlink_counts[rawDataObj.url.encode("utf-8")] += len(urls)

        download_counts[rawDataObj.url.encode("utf-8")] += 1

        urls = set(imap_multiple(urls, stripTrailingSlash, removeFragment))

        # Define url patterns to match and it's max count
        patterns = OrderedDict()
        patterns['news/view_news(php)?'] = 50
        patterns['calendar.ics.uci.edu/calendar.php'] = 0
        patterns['ganglia.ics.uci.edu'] = 0
        patterns['.*'] = -1  # Any number of occurrence

        filters = [ isHttpOrHttps,
                    isInDomain("ics.uci.edu"),
                    isNotAsset,
                    queryCount(300,query_counts),
                    patternCount(patterns, pattern_counts),
                    linkCount(lambda x: x < 1, visit_counts)
                  ]
        urls = applyFilters(filters, urls)

        # print(list(urls), visit_counts)

        outputLinks = urls
    except Exception as e:
        print(e)

    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded.
    The frontier takes care of that.

    Suggested library: lxml
    '''

    return outputLinks


def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url.encode("utf-8"))
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
               and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                + "|thmx|mso|arff|rtf|jar|csv" \
                                + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False
