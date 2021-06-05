from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url                # home page url
        self.page_url = page_url                # page we are trying to parse url
        self.links = set()                      # when crawling page, store all links we found in this set

    def handle_starttag(self, tag, attrs):
        if tag == 'a':                          # sees if starting tag is link
            for(attribute, value) in attrs:
                if attribute == 'href':
                    full_url = parse.urljoin(self.base_url, value)       # if value is a relative url (ending part of url without home page url), we are combining urls to get full url
                    self.links.add(full_url)
    
    def page_links(self):
        return self.links

    def error(self, message):
        pass