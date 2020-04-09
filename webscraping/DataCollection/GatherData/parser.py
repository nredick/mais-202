import requests
from bs4 import BeautifulSoup


class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return [self.parse_html_table(table) \
                for table in soup.find_all('table')]

    def parse_html_table(self, table):
        l = []
        for row in table.find_all('tr'):
            l.append(row.get_text()[42:])
        return l
