import logging
from datamodel.search.Yicongh1ZicanlHwo_datamodel import Yicongh1ZicanlHwoLink, OneYicongh1ZicanlHwoUnProcessedLink
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

from urlparse import urlparse, parse_qs
from uuid import uuid4

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(Yicongh1ZicanlHwoLink)
@GetterSetter(OneYicongh1ZicanlHwoUnProcessedLink)
class CrawlerFrame(IApplication):
    app_id = "Yicongh1ZicanlHwo"

    def __init__(self, frame):
        self.app_id = "Yicongh1ZicanlHwo"
        self.frame = frame


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
        for link in unprocessed_links:
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(Yicongh1ZicanlHwoLink(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
def extract_next_links(rawDataObj):
    outputLinks = []
    print rawDataObj.url
    try:
        doc = html.document_fromstring(rawDataObj.content)
        doc.make_links_absolute(rawDataObj.final_url if rawDataObj.is_redirected else rawDataObj.url)

        urls = [i[2] for i in doc.iterlinks()]
        for i  in range(len(urls)):
            if "?" in urls[i]:
                urls[i] = urls[i][:urls[i].index("p")]
        print(urls)

        outputLinks.extend(urls)
    except:
        pass


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
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False

