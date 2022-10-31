from multiprocessing.dummy import freeze_support
import requests
import json
import undetected_chromedriver as uc

from bs4 import BeautifulSoup

from backend.getRectangle import get_rectangle_bounds
from backend.TSL import test
from backend.sites.Avito import check

#url = "https://market-backend.api.2gis.ru/5.0/realty/markers?platform_code=34&category_ids=70241201812761646&point1=37.567998629456895,55.704251748170435&point2=37.5902637968234,55.69167723619958&locale=ru_RU"
#
#response = requests.request("GET", url)
#res = response.json()
#geo_id = res['result']['items'][0]['building_id']
#
#url = "https://market-backend.api.2gis.ru/5.0/realty/items?locale=ru_RU&platform_code=34&category_ids=70241201812761646&point1=37.567998629456895,55.704251748170435&point2=37.5902637968234,55.69167723619958&page=1&page_size=20&geo_id="
#
#url += geo_id
#response = requests.request("GET", url)
#res = response.json()
#
#with open('data.json', 'w', encoding='utf-8') as outfile:
#    json.dump(res, outfile, indent=4, ensure_ascii=False)


#Start
def parse_2gis():
    data = dict()
    api_parser(data)
    with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def api_parser(data):
    # Use get_rectangle_bounds() for x, y
    url = get_url_parser()
    response = requests.request("GET", url)
    res = response.json()
    for i in range(len(res['result']['items'])):
        data[str(i)] = dict()
        data[str(i)]['meta'] = {'building_id': get_geo_id(),
                                'flat_id': res['result']['items'][i]['product']['id']}

        if len(res['result']['items'][i]['product']['attributes']) == 4:
            data[str(i)]['content'] = {'needed': {
                                                  'address': create_address(res['result'], i),
                                                  'num_rooms': res['result']['items'][i]['product']['attributes'][1]['value']
                                                },
                                       'correcting': {
                                                      'floor': res['result']['items'][i]['product']['attributes'][3]['value'],
                                                      'square_flat': res['result']['items'][i]['product']['attributes'][2]['value']
                                                    }
                                    }           
        else:
            data[str(i)]['content'] = {'needed': {
                                                  'address': create_address(res['result'], i),
                                                  'num_rooms': res['result']['items'][i]['product']['attributes'][0]['value']
                                                },
                                       'correcting': {
                                                      'floor': res['result']['items'][i]['product']['attributes'][2]['value'],
                                                      'square_flat': res['result']['items'][i]['product']['attributes'][1]['value']
                                                    }
                                    }      
        #page_parser(data, i)         Not worked!         

def create_address(res, num):
    adress_str = 'Москва, '
    adress_str += res['items'][num]['building']['adm_div'][3]['name'] + ', '
    adress_str += res['items'][num]['building']['address']['components'][0]['street'] + ', '
    adress_str += res['items'][num]['building']['address']['components'][0]['number']
    return adress_str

def get_geo_id(x=("37.567998629456895", "55.704251748170435"), y=("37.5902637968234", "55.69167723619958")):
    #bounds = get_rectangle_bounds(coord)
    url_data = {
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": x, #("37.567998629456895", "55.704251748170435")
        "point2": y, #("37.5902637968234", "55.69167723619958")
        "locale": "ru-RU",
    }
    
    url = "https://market-backend.api.2gis.ru/5.0/realty/markers?"

# Useless
    for key, value in url_data.items():
        if type(value) is not str:
            value = ",".join(value)
        url += key + "=" + value + "&"
    url = url[:-1]
    response = requests.request("GET", url)
    res = response.json()
    geo_id = res['result']['items'][0]['building_id']
    return geo_id

def get_url_parser(x=("37.567998629456895", "55.704251748170435"), y=("37.5902637968234", "55.69167723619958")):
    geo_id = get_geo_id(x, y)
    url_data = {
        "locale": "ru_RU",
        "platform_code": "34",
        "category_ids": "70241201812761646",
        "point1": x, # ("37.567998629456895", "55.704251748170435")
        "point2": y, #("37.5902637968234", "55.69167723619958"),
        "page": "1",
        "page_size": "20",
        "geo_id": geo_id
    }

    url = "https://market-backend.api.2gis.ru/5.0/realty/items?"

    # Useless
    for key, value in url_data.items():
        if type(value) is not str:
            value = ",".join(value)
        url += key + "=" + value + "&"
    url = url[:-1]
    return url

#Not worked
def page_parser(data, elem):
    url = get_url_page(data[str(elem)]['meta'])
    print(url)
    try:
        driver = uc.Chrome()
        pageSource = test(url, driver=driver)
    except Exception as exception:
        print(exception)
    print(pageSource)
    
    
def get_url_page(data):
    url = 'https://2gis.ru/moscow/realty/sale/ad/' + data['flat_id']
    return url