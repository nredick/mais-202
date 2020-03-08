import csv
import multiprocessing
import time
from parser import HTMLTableParser


# crawl function that takes a single html response and parses the data;
# implemented via multiprocess.Process in main()
def crawl_processing(args, w, count, hp):
    print(f'{time.ctime()}: Write data from response {count+1} to csv.')
    table = hp.parse_url(args)
    with w:
        write = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in table:
            write.writerow(row)


# return all urls as a list of strings based on offset pattern and base url
def get_urls():
    # make a list with all of the urls of the data to be scraped
    num = 0
    urls = []
    for i in range(4747):  # 4747
        urls.append("https://geogallery.si.edu/portal?has_media=true&offset=" + str(num))
        num += 10
    return urls


def main():
    hp = HTMLTableParser()
    OUT = 'data2.csv'  # output filename for parsed html data
    w = open(f'../DataCollection/output_files/{OUT}', 'w')  # open output file as w

    # keep track of program runtime
    print(f'{time.ctime()}: Begin data collection process.')
    start_time = time.time()

    # step 1: create urls
    print(f'{time.ctime()}: Create URLs.')
    step_time = time.time()
    urls = get_urls()
    print(f'{time.ctime()}: URLs successfully created.\nStep Runtime: {time.time() - step_time}')

    # step 2: parse all the html response data and output to OUT as a csv; each line is
    # one record of data
    print(f'{time.ctime()}: Parse HTML data.')
    step_time = time.time()
    # set up multiprocessing to parse data faster
    for count, r in enumerate(urls):
        p = multiprocessing.Process(target=crawl_processing, args=(r, w, count, hp))
        p.start()
        p.join()
    print(f'{time.ctime()}: HTML data parsed.\nStep Runtime: {time.time() - step_time}')

    print(f'{time.ctime()}: Data collection process completed.\nProgram Runtime: {time.time() - start_time}')


if __name__ == "__main__":
    main()