import threading
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.irn.ru/kvartiry/moskva/ceny-po-rayonam/'


class Parser(threading.Thread):
    def __init__(self):
        super().__init__()
        self.prices_by_district = {}

    def run(self):
        while True:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            all_prices = soup.findAll('table', class_='space-medium-top list1 table-currency')[0].find_all('tr')
            for data in all_prices[2:]:
                data = list(map(lambda y: y.replace('\xa0', ''), filter(lambda x: x, data.text.replace('\t', '').split('\n'))))
                self.prices_by_district[data[-4][:-1]] = int(data[-2])
            print(self.prices_by_district)
            time.sleep(60)


