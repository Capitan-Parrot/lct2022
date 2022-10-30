import ssl
from pprint import pprint

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_


def cheak1(pageSource):
    start1 = pageSource.find('data-marker="item-view/title-info">')
    end1 = pageSource.find('</span>', start1)
    return pageSource[start1 + len('data-marker="item-view/title-info">'):end1].replace('&nbsp;','')

def cheak2(pageSource):
    start1 = pageSource.find('class="params-paramsList-zLpAu"')
    end1 = pageSource.find('</ul>', start1)
    return pageSource[start1 + len('class="params-paramsList-zLpAu"'):end1].replace('&nbsp;','')


def cheak(pageSource, start_str, end_str):
    start=pageSource.find(start_str)
    end = pageSource.find(end_str, start)
    return pageSource[start + len(start_str):end].replace('&nbsp;', '')


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
pageSource=str(r.text)
# print(pageSource)


print(cheak(pageSource,'data-marker="item-view/title-info">','</span>'))#3-к. квартира, 73,9м², 1/5эт.

buff_str=cheak2(pageSource)
print(buff_str)
for i in range(10):
    print(cheak(buff_str,'</span>','</li>'))
    buff_str.replace('</span>','',1)
    buff_str.replace('</li>','', 1)


