import csv
import requests
from threading import Thread
from multiprocessing import JoinableQueue
import shutil
import time
from pathlib import Path
import os


def crawl(queue, output_folder):
    while not queue.empty():
        work = queue.get()
        print(time.ctime(), f'Starting thread for {work[1]}{work[0]}')
        make_request(work=work, output_folder=output_folder)
        queue.task_done()


def make_request(work, output_folder):
    count, name, link = [*work]
    response = requests.get(link, stream=True)
    filename = Path(f'{output_folder}/{name}{count}.jpeg')
    filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
    with open(filename, 'wb') as img:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, img)
        del response


def main():
    input_file = 'parsed_data.csv'
    output_folder = '/Users/nathalieredick/workspaces/mais202/datacollection/output_files/Images'

    if not os.path.isdir(f'{output_folder}'):
        os.makedirs(f'{output_folder}')
    queue = JoinableQueue()

    with open(f'/Users/nathalieredick/workspaces/mais202/datacollection/output_files/{input_file}', 'r') as r:
        read = csv.reader(r, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        count = 0
        read = list(read)
        for i in range(len(read)):
            index = i
            if count > 32700:
                index = i + count
            name = read[index][0]
            link = read[index][1]

            args = [count, name, link]
            queue.put(args)
            count += 1
            if count == 32700:
                num_threads = 50
                for n in range(num_threads):
                    worker = Thread(target=crawl, args=(queue, output_folder,))
                    worker.setDaemon(True)
                    worker.start()
                queue.join()


if __name__ == "__main__":
    main()
