import ssl
from pprint import pprint

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_

from backend.getRectangle import get_rectangle_bounds


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


x, y = get_rectangle_bounds([55.697965, 37.579133])

data = {
    "categoryId": "24",
    "locationId": '637640',
    "searchArea[lonLeft]": x[1],
    "searchArea[latBottom]": y[0],
    "searchArea[lonRight]": y[1],
    "searchArea[latTop]": x[0],
}
session = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
session.mount("https://", adapter)
url = 'https://www.avito.ru/moskva/kvartiry/3-k._kvartira_739m_15et._2411657289'
try:
    r = session.request('GET', url)

    pprint(r.text)
except Exception as exception:
    print(exception)