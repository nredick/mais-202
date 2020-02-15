import csv
import requests
from threading import Thread
from multiprocessing import JoinableQueue
import shutil
import time


def crawl(queue, output_folder):
    while not queue.empty():
        work = queue.get()
        if work[0] % 100 == 0:
            time.sleep(5)
        print(time.ctime(), f'Starting thread for {work[1]}{work[0]}')
        make_request(work=work, output_folder=output_folder)


def make_request(work, output_folder):
    count, name, link = [*work]
    response = requests.get(link, stream=True)
    with open(f'{output_folder}/{name}{count}.jpeg', 'wb') as img:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, img)
        del response


def main():
    input_file = 'parsed_data.csv'
    output_folder = '../DataCollection/output_files/Images'
    queue = JoinableQueue(maxsize=0)
    with open(f'../DataCollection/output_files/{input_file}', 'r') as r:
        read = csv.reader(r, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        prev_name = ''
        count = 0
        for name, link in list(read):
            if name == prev_name:
                args = [count, name, link]
                queue.put(args)
                #make_request(args, output_folder)
                count += 1
            else:
                count = 0
                prev_name = name

    num_threads = 150
    for n in range(num_threads):
        worker = Thread(target=crawl, args=(queue, output_folder,))
        worker.setDaemon(True)
        worker.start()
    queue.join()


if __name__ == "__main__":
    main()
