from urllib2 import urlopen
from link_finder import LinkFinder
from general import *

class Spider:
    # Class variables(shared among all instances)
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider', Spider.base_url)

    # first spider starts with project folder and the basic files
    # links need to be converted to set
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name,Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' crawling' + page_url)
            print('Queue' + str(len(Spider.queue)) + '|Crawled:' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            # print Spider.queue
            Spider.queue.remove(page_url) # remove from wait list
            Spider.crawled.add(page_url) # put to crawled list
            Spider.update_files()

    # connects to a site, takes the html converts it to proper string format, passes to linkfinder, finds all urls and
    # returns the set of links
    @staticmethod
    def gather_links(page_url):
        html_string = ''

        #print response
        #print(response.getheader('Content-Type'))
        try:
            response = urlopen(page_url)
            #response = requests.get(page_url).text
            # print(response.getheader('Content-Type'))
            #if response.getheader('Content-Type') == 'text/html':

            extractedheaders = response.headers;
            if 'text/html' in extractedheaders.headers[2]:
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print('Error: cannot crawl page ' + str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)


    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)











