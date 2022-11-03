import os
import time

import grequests
import requests
import json

from backend.utils.checkIsAnalog import check_is_analog
from backend.utils.getRectangle import get_rectangle_bounds
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


def get_markers(x, y):
    data = {
        "locale": "ru_RU",
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": f'{x[0]}, {x[1]}',
        "point2": f'{y[0]}, {y[1]}'
    }
    url = "https://market-backend.api.2gis.ru/5.0/realty/markers?"
    response = requests.get(url, params=data)
    return response.json()['result']['items']


def get_buildings(x, y, markers):
    data = {
        "locale": "ru_RU",
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": f'{x[0]}, {x[1]}',
        "point2": f'{y[0]}, {y[1]}',
        "page": "1",
        "page_size": "20",
    }
    buildings = (
        grequests.get('https://market-backend.api.2gis.ru/5.0/realty/items?',
                      params=data | {'geo_id': j['building_id']}) for j in markers)
    return iter(grequests.map(buildings))


def get_info_buildings(buildings_id):
    data = {
        "locale": "ru_RU",
        'key': os.getenv('2GIS_KEY'),
        'fields': "items.locale,items.flags,search_attributes,items.adm_div,items.city_alias,items.region_id,items.segment_id,items.reviews,items.point,request_type,context_rubrics,query_context,items.links,items.name_ex,items.org,items.group,items.dates,items.external_content,items.contact_groups,items.comment,items.ads.options,items.email_for_sending.allowed,items.stat,items.stop_factors,items.description,items.geometry.centroid,items.geometry.selection,items.geometry.style,items.timezone_offset,items.context,items.level_count,items.address,items.is_paid,items.access,items.access_comment,items.for_trucks,items.is_incentive,items.paving_type,items.capacity,items.schedule,items.floors,ad,items.rubrics,items.routes,items.platforms,items.directions,items.barrier,items.reply_rate,items.purpose,items.attribute_groups,items.route_logo,items.has_goods,items.has_apartments_info,items.has_pinned_goods,items.has_realty,items.has_exchange,items.has_payments,items.has_dynamic_congestion,items.is_promoted,items.congestion,items.delivery,items.order_with_cart,search_type,items.has_discount,items.metarubrics,broadcast,items.detailed_subtype,items.temporary_unavailable_atm_services,items.poi_category,items.structure_info.material,items.structure_info.floor_type,items.structure_info.gas_type,items.structure_info.year_of_construction,items.structure_info.elevators_count,items.structure_info.is_in_emergency_state,items.structure_info.project_type",
        "id": buildings_id
    }
    url = "https://catalog.api.2gis.com/3.0/items/byid?"
    response = requests.get(url, params=data)
    return response.json()


def api_parser(base_flats):
    x_coord, y_coord, geo_id = get_coords_by_address(base_flats[base_flats.keys()[0]]['address'])
    x, y = get_rectangle_bounds([x_coord, y_coord])
    markers = get_markers(x, y)
    buildings = get_buildings(x, y, markers)
    info_buildings = get_info_buildings(','.join(j['building_id'] for j in markers))
    # exit()
    flats = {}
    for building in buildings:
        # data['geo_id'] = building['building_id']
        # url = "https://market-backend.api.2gis.ru/5.0/realty/items?"
        # response = requests.get(url, params=data)
        res = building.json()['result']['items']
        for i in range(len(res)):
            if res[i]['product']['attributes'][0]['value'] != 'Квартира':
                continue
            flat = {'meta': {'building_id': res[i]['building']['address']['building_id'],
                             'flat_id': res[i]['product']['id']}}
            if len(res[i]['product']['attributes']) == 4:
                flat['content'] = {
                    'required': {
                        'address': create_address(res[i]['building']),
                        'num_rooms': res[i]['product']['attributes'][1]['value'],
                        'building_segment': '',
                        'building_num_floors': 0,
                        'building_material': ''
                    },
                    'correcting': {
                        'floor': res[i]['product']['attributes'][3]['value'],
                        'square_flat': res[i]['product']['attributes'][2]['value'],
                        'square_kitchen': 0,
                        'distance_from_metro': 0,
                        'nearest_station': '',
                        'condition': ''
                    }
                }
            else:
                flat['content'] = {
                    'required': {
                        'address': create_address(res[i]['building']),
                        'num_rooms': res[i]['product']['attributes'][0]['value'],
                        'building_segment': '',
                        'building_num_floors': 0,
                        'building_material': ''
                    },
                    'correcting': {
                        'floor': res[i]['product']['attributes'][2]['value'],
                        'square_flat': res[i]['product']['attributes'][1]['value'],
                        'square_kitchen': 0,
                        'distance_from_metro': 0,
                        'nearest_station': '',
                        'condition': ''
                    }
                }
            if check_is_analog(flat['content']['required'], base_flats['content']['required']['num_rooms']):
                flats[flat['content']['required']['num_rooms']].append(flat)
    return flats


def parse_2gis(base_flats=None):
    if base_flats is None:
        base_flats = [{'num_rooms': 1, 'address': 'Москва, Ферсмана, 3 к1'}]
    data = api_parser(base_flats)
    return data
    # with open('data.json', 'w', encoding='utf-8') as outfile:
    #     json.dump(data, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    load_dotenv()
    tick = time.time()
    print(time.time() - tick)
