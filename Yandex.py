from pprint import pprint

from requests import get

from backend.getRectangle import get_rectangle_bounds

x, y = get_rectangle_bounds([55.697965, 37.579133])
data = {
    "rgid": "741964",
    "type": 'SELL',
    "category": 'APARTMENT',
    "leftLongitude": x[1],
    "bottomLatitude": y[0],
    "rightLongitude": y[1],
    "topLatitude": x[0],
    "zoom": 20,
    "count": 1000
}
print(data)
url = 'https://realty.ya.ru/gate/map/offers-points-with-counter/?'
res = get(url, params=data)
print(res.url)
res = res.json()
pprint([elem['id'] for elem in res['response']['points']])
