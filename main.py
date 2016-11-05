import threading
from Queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'Webcrawler'
HOME_PAGE= 'https://thenewboston.com'
DOMAIN_NAME = get_domain_name(HOME_PAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME,HOME_PAGE,DOMAIN_NAME)

# check if there are items in the queue and crawl
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    crawled_links = file_to_set(CRAWLED_FILE)

    # print queued_links
    if len(queued_links) > 0 and len(crawled_links) <= 1000:
        print (str(len(queued_links)) + ' links in queue')
        create_jobs()

# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

# Create worked threads (will die when main exits)

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t =threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

create_workers()
crawl()
