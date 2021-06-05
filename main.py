import threading                    # our spiders
from queue import Queue             # their jobs
from spider import Spider
from domain import *
from general import *

# multithreading
# calls the spider over and over
PROJECT_NAME = 'seed'                               # video 15
HOME_PAGE = 'https://seed.edu/'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8           # depends on operating system

thread_queue = Queue()
Spider(PROJECT_NAME, HOME_PAGE, DOMAIN_NAME)        # first spider

# Create worker threads (spiders); will die when main exits
def create_threads():
    for _ in range(NUMBER_OF_THREADS):              # putting an '_' disregards that value and we just loop through NUMBER_OF_THREADS times
        t = threading.Thread(target=work)           # creates 8 threads that just work
        t.daemon = True
        t.start()                                   # tells the threads to start working

# Do next job in queue
def work():
    while True:
        url = thread_queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()                    # thread ready for next job

# Each queued link is a new job for the spiders
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawl()

# Check if there are items in the queue; if there are, rest of spiders will crawl them using multithreading
def crawl():                                    # video 16
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()

create_threads()
crawl()