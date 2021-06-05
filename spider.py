from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

class Spider:

    # class variables shared among all instances)       # video 8
    project_name = ''
    base_url = ''       # home page url
    domain_name = ''
    queue_file = ''             
    crawled_file = ''
    queue_set = set()           # dont want to write to file every time we come across link cause that's slow;
    crawled_set = set()         # using variables that get stored to RAM is a lot faster than files stored on hard drive

    def __init__(self, project_name, base_url, domain_name):       # video 9
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.First_Spider()
        self.crawl_page('First spider', Spider.base_url)        # create first spider to crawl home page url
        # first spider has the unique task of creating project directory and two data files (queue and crawled)

    @staticmethod
    def First_Spider():             # video 10
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # crawls page
    @staticmethod                   # video 11
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' is now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)            # moving link from waitlist to crawled list when crawled
            Spider.update_files()

    # pass in page url, get the html, and convert bytes into readable characters
    @staticmethod
    def gather_links(page_url):     # video 12
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: cannot crawl page')
            return set()                            # there were not any links on crawled page
        return finder.page_links()

    # takes a set of links and adds it to the existing waitlist of links
    @staticmethod
    def add_links_to_queue(links):     # video 13   
        for url in links:                       # loops through each link one by one
            if url in Spider.queue:             # if link already in queue, does not add it and continues to next item in list
                continue
            if url in Spider.crawled:           # if link already in crawled, does not add it and continues to next item in list
                continue 
            if Spider.domain_name not in url:   # dont want to add link that does not have domain_name
                continue
            Spider.queue.add(url)               # adds link to waitlist

    @staticmethod
    def update_files():       # save data in sets to a file
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)