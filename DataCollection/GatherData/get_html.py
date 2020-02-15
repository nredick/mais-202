# imports
import time
from multiprocessing import JoinableQueue
from threading import Thread
import requests


class GetHTML:
    # global variables
    def __init__(self):
        self.RESPONSES = []  # holds html responses from each url get-request
        self.QUEUE = JoinableQueue(maxsize=0)  # Joinable queue to pass urls to worker; no size limit

    # define crawl function for multi threading get-requests
    def crawl_threading(self):
        while not self.QUEUE.empty():
            # fetch new work from the queue
            work = self.QUEUE.get()
            # sends get request for each method on each task from queue via a worker
            response = requests.get(work)
            print(f'{time.ctime()}: {work}\tRequest status: {response.status_code}')

            # system exit if get request failed
            if response.status_code != 200:
                print("URL request failed.")
                break
            else:
                #print(response.content)
                self.RESPONSES.append([response.content])
                self.QUEUE.task_done()  # signals that a task has been finished and a thread is released

    # get html responses
    def get_html(self):  # URLS is a list of urls
        num_threads = 30
        # set up threads that take url paths from the queue and pass them through
        print(time.ctime(), 'Number of threads:', num_threads)
        for z in range(num_threads):
            worker = Thread(target=self.crawl_threading)
            worker.setDaemon(True)
            worker.start()

        # wait until all threads have been processed to continue
        self.QUEUE.join()
        return self.RESPONSES

    def create_queue(self, URLS):
        for row in URLS:
            print(time.ctime(), f'Adding to queue: {row}')
            self.QUEUE.put(row)