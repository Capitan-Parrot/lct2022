import os
import requests
import json
from backend.getRectangle import get_rectangle_bounds
from dotenv import load_dotenv


# Start


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


def create_address(building):
    full_address = f"Москва, {building['adm_div'][3]['name']}, {building['address']['components'][0]['street']}," \
                   f" {building['address']['components'][0]['number']}"
    return full_address


def api_parser(address):
    x_coord, y_coord, geo_id = get_coords_by_address(address)
    x, y = get_rectangle_bounds([x_coord, y_coord])
    data = {
        "locale": "ru_RU",
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": f'{x[0]}, {x[1]}',
        "point2": f'{y[0]}, {y[1]}'
    }
    url = "https://market-backend.api.2gis.ru/5.0/realty/markers?"
    response = requests.get(url, params=data)
    buildings = response.json()['result']['items']
    data = {
        "locale": "ru_RU",
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": f'{x[0]}, {x[1]}',
        "point2": f'{y[0]}, {y[1]}',
        "page": "1",
        "page_size": "20",
    }
    flats = []
    for building in buildings:
        data['geo_id'] = building['building_id']
        url = "https://market-backend.api.2gis.ru/5.0/realty/items?"
        response = requests.get(url, params=data)
        res = response.json()['result']['items']
        flats_in_building = []
        for i in range(len(res)):
            if res[i]['product']['attributes'][0]['value'] != 'Квартира':
                continue
            flats_in_building.append({})
            flats_in_building[-1]['meta'] = {'building_id': res[i]['building']['address']['building_id'],
                                             'flat_id': res[i]['product']['id']}

            if len(res[i]['product']['attributes']) == 4:
                flats_in_building[-1]['content'] = {
                    'needed': {
                        'address': create_address(res[i]['building']),
                        'num_rooms': res[i]['product']['attributes'][1]['value']
                    },
                    'correcting': {
                        'floor': res[i]['product']['attributes'][3]['value'],
                        'square_flat': res[i]['product']['attributes'][2]['value']
                    }
                }
            else:
                flats_in_building[-1]['content'] = {
                    'needed': {
                        'address': create_address(res[i]['building']),
                        'num_rooms': res[i]['product']['attributes'][0]['value']
                    },
                    'correcting': {
                        'floor': res[i]['product']['attributes'][2]['value'],
                        'square_flat': res[i]['product']['attributes'][1]['value']
                    }
                }
        flats.extend(flats_in_building)
    return flats


def parse_2gis(address='Москва, Ферсмана, 3 к1'):
    data = api_parser(address)
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    load_dotenv()
    parse_2gis()
