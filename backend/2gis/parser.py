import os
import time
from pprint import pprint
import requests

from backend.filters import filter_floors, filter_material, filter_segment
from backend.utils.getSession import session
from backend.findFlats.getRectangle import get_rectangle_bounds


def get_coords_by_address(address):
    data = {
        'q': address,
        'fields': 'items.point',
        'key': os.getenv('2GIS_KEY')
    }
    url = 'https://catalog.api.2gis.com/3.0/items/geocode?'
    response = requests.get(url, params=data)
    res = response.json()['result']['items'][0]
    x_coord, y_coord, geo_id = res['point']['lat'], res['point']['lon'], res['id'].split('_')[0]
    return x_coord, y_coord, geo_id


def get_offers(x, y, base_flat):
    data = {
        "jsonQuery": {
            "_type": "flatsale",
            "bbox": {
                "type": "term",
                "value": [[x[0], y[1]], [y[0], x[1]]]
            },
            "floorn": filter_floors(int(base_flat['building_num_floors'])),
            "house_year": filter_segment(base_flat['building_segment']),
            "house_material": filter_material(base_flat['building_material'])
        }
    }
    offers = session.request('POST', "https://api.cian.ru/search-offers/v2/search-offers-desktop/", json=data)
    return offers.json()['data']['offersSerialized']


def api_parser(base_flats):
    # x_coord, y_coord, geo_id = get_coords_by_address(base_flats[list(base_flats.keys())[0]]['address'])
    x_coord, y_coord, geo_id = 55.697948, 37.579112, 4504235282605884
    x, y = get_rectangle_bounds([x_coord, y_coord])
    offers = get_offers(x, y, base_flats[list(base_flats.keys())[0]])
    flats = {num_room: [] for num_room in base_flats}
    for offer in offers:
        flat = {
            'required': {
                'address': offer['geo']['userInput'],
                'num_rooms': offer['roomsCount'],
                'building_year': offer['building']['buildYear'],
                'building_num_floors': offer['building']['floorsCount'],
                'building_material': offer['building']['materialType']
            },
            'correcting': {
                'floor': offer['floorNumber'],
                'square_flat': float(offer['totalArea']),
                'square_kitchen': float(offer['kitchenArea']),
                'metro_distance': float(offer['geo']['railways'][0]['distance']),
                'nearest_station': offer['geo']['railways'][0]['name'],
                'balcony / loggia': (offer['balconiesCount'] != 0) or (offer['loggiasCount'] != 0),
                'condition': offer['geo']['railways'][0]['name'],
            },
            'price': offer['bargainTerms']['priceRur']
        }
        pprint(flat)
        num_rooms = flat['required']['num_rooms']
        if num_rooms not in base_flats:
            print('wtf')
            continue
        flats[flat['required']['num_rooms']].append(flat)
    return flats


def parse_2gis(base_flats=None):
    if base_flats is None:
        base_flats = [{'num_rooms': 1, 'address': 'Москва, Ферсмана, 3 к1'}]
    data = api_parser(base_flats)
    return data
    # with open('data.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(data, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    tick = time.time()
    print(parse_2gis({1: {"address": "Москва, проспект 60-летия Октября, 11",
                          "num_rooms": 1,
                          "building_segment": "Cтарый жилой фонд",
                          "building_num_floors": 16,
                          "building_material": "Панель",
                          "floor": 10,
                          "square_flat": 25.0,
                          "square_kitchen": 10.0,
                          "has_balcony": False,
                          "metro_distance": 10,
                          "condition": "economy"}}))
    print(time.time() - tick)
