import os
import requests
import ssl
import sys
import threading                    # our spiders
import urllib.request
from queue import Queue             # their jobs
from spider import Spider
from domain import *
from general import *

# multithreading
# calls the spider over and over
# PROJECT_NAME = 'seed'                               # video 15
# HOME_PAGE = 'https://seed.edu/'
# DOMAIN_NAME = get_domain_name(HOME_PAGE)
# QUEUE_FILE = PROJECT_NAME + '/queue.txt'
# CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
# NUMBER_OF_THREADS = 8           # depends on operating system
ssl._create_default_https_context = ssl._create_unverified_context

class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


print('Welcome to our CS172 Final Project. Please type a URL to crawl below:')
PROJECT_NAME = 'MAJ-Project'                               # video 15
HOME_PAGE = str(input())
req = requests.get(HOME_PAGE)
if (not req.status_code == 200):
    print('The URL you entered does not exist')
    exit()
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
print('Please enter the number of pages to crawl below:')
PAGES_TO_CRAWL = int(input())
print('Please enter the number of levels(hops/hyperlinks) away from the seed URL to crawl:')
NUM_HOPS = int(input())
CURR_HOPS = 0
print('Please enter the number of threads to use in the crawler:')
NUMBER_OF_THREADS = int(input())           # depends on operating system

thread_queue = Queue()
threads = []
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME, PAGES_TO_CRAWL)        # first spider

# Create worker threads (spiders); will die when main exits
def create_threads():
    for _ in range(NUMBER_OF_THREADS):              # putting an '_' disregards that value and we just loop through NUMBER_OF_THREADS times
        t = StoppableThread(target=work)           # creates n threads that just work
        t.daemon = True
        t.start()   
        threads.append(t)                                # tells the threads to start working

# Do next job in queue
def work():
    while True:
        url = thread_queue.get()
        crawled_links = file_to_set(CRAWLED_FILE)
        if (not len(crawled_links) >= PAGES_TO_CRAWL):
            Spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()                    # thread ready for next job

# Each queued link is a new job for the spiders
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawled_links = file_to_set(CRAWLED_FILE)
    if (len(crawled_links) >= PAGES_TO_CRAWL):
        return None
    else:
        crawl()

# Check if there are items in the queue; if there are, rest of spiders will crawl them using multithreading
def crawl():                                    # video 16
    queued_links = file_to_set(QUEUE_FILE)
    crawled_links = file_to_set(CRAWLED_FILE)
    if (len(crawled_links) >= PAGES_TO_CRAWL):
        return None
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        global CURR_HOPS
        CURR_HOPS += 1
        if not CURR_HOPS > NUM_HOPS:
            create_jobs()

def dlHTML():
    i = 1
    crawled_links = file_to_set(CRAWLED_FILE)
    if not os.path.exists('MAJ-Project/HTML'):
        os.makedirs('MAJ-Project/HTML')
    for link in crawled_links:
        if not 'mailto:' in link:
            page = link.split('/')[-1]
            pathString = 'MAJ-Project/HTML/' + 'post-' + str(i) + '.html'
            f = open(pathString, 'w+')
            urllib.request.urlretrieve(link, pathString)
            i += 1

create_threads()
crawl()
print("Successfully crawled", end=" ")
print(PAGES_TO_CRAWL, end=" ")
print("pages.")
if (len(file_to_set(CRAWLED_FILE)) != PAGES_TO_CRAWL):
    print('The program crawled all hyperlinks', end=' ')
    print(NUM_HOPS, end=' ')
    print('hops away before crawling a total of', end=" ")
    print(PAGES_TO_CRAWL, end=' ')
    print('pages.')
dlHTML()

# exit()