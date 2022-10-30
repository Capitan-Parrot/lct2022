import ssl
from pprint import pprint

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_


def cheak(pageSource, start_str, end_str):
    start = pageSource.find(start_str)
    end = pageSource.find(end_str, start)
    pageSource=pageSource[start + len(start_str):end].replace('&nbsp;', '')
    # pageSource=pageSource[start + len(start_str):end].replace('xa0;', '')
    return pageSource


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


url = "https://www.avito.ru/moskva/kvartiry/3-k._kvartira_739m_15et._2411657289"
session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)
r = session.request('GET', url)
pageSource = str(r.text)
# print(pageSource)

print(cheak(pageSource, 'data-marker="item-view/title-info">', '</span>'))  # 3-к. квартира, 73,9м², 1/5эт.

buff_str = cheak(pageSource, 'class="params-paramsList-zLpAu"', '</ul>')#отдельно сохраняю первый список с параметраии 

list1 = [{'Количество комнат:': 0},  #список словарей для хранения информации о квартире
         {'Общая площадь:': 0},      #PS я давно не работат со словорями, может это можно как-то более красиво реализовать
         {'Площадь кухни:': 0},
         {'Жилая площадь:': 0},
         {'Этаж:': 0},
         {'Тип комнат:': 0},
         {'Высота потолков:': 0},
         {'Санузел:': 0},
         {'Окна:': 0},
         {'Ремонт:': 0},
         {'Способ продажи:': 0}]

list1_sub = ['Количество комнат:', 'Общая площадь:', 'Площадь кухни:', 'Жилая площадь:', 'Этаж:', 'Тип комнат:',
             'Высота потолков:', 'Санузел:', 'Окна:', 'Ремонт:', 'Способ продажи:']

for i in range(10):                 #парселинг отдельно списка с параметрами
    list1[i][list1_sub[i]]=cheak(buff_str, '</span>', '</li>')  #обращение к элементу словоря
    print(cheak(buff_str, '</span>', '</li>'))
    buff_str = buff_str[:buff_str.find('</span>')] + buff_str[buff_str.find('</li>') + 5:]

print(list1)
