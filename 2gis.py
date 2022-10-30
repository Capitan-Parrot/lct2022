from pprint import pprint

import requests

url = "https://market-backend.api.2gis.ru/5.0/realty/markers?platform_code=34&category_ids=70241201812761646&point1=37.567998629456895,55.704251748170435&point2=37.5902637968234,55.69167723619958&locale=ru_RU"

response = requests.request("GET", url)
res = response.json()
geo_id = res['result']['items'][0]['building_id']

url = "https://market-backend.api.2gis.ru/5.0/realty/items?locale=ru_RU&platform_code=34&category_ids=70241201812761646&point1=37.567998629456895,55.704251748170435&point2=37.5902637968234,55.69167723619958&page=1&page_size=20&geo_id="

url += geo_id
response = requests.request("GET", url)
res = response.json()
pprint(res['result']['items'])

