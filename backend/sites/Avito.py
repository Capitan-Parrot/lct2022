import time

import requests

from backend.TSL import get_page_content, get_url, test
from backend.getRectangle import get_rectangle_bounds


def get_avito(x, y):
    data = {
        "categoryId": "24",
        "locationId": '637640',
        "searchArea[lonLeft]": x[1],
        "searchArea[latBottom]": y[0],
        "searchArea[lonRight]": y[1],
        "searchArea[latTop]": x[0],
    }
    url = 'https://www.avito.ru/js/1/map/items?'
    try:
        r = test(url, data).json()
        avito_urls = ['https://www.avito.ru' + elem['urlPath'] for elem in r['items']]
        for elem in avito_urls:
            print(elem, get_flat_params(elem).get('Количество комнат:'))
            time.sleep(0.1)
    except Exception as exception:
        print(exception)


def check(pageSource, start_str, end_str):
    start = pageSource.find(start_str)
    end = pageSource.find(end_str, start)
    pageSource = pageSource[start + len(start_str):end].replace('&nbsp;', '').replace('\xa0', ' ')
    # pageSource=pageSource[start + len(start_str):end].replace('xa0;', '')
    return pageSource


def get_flat_params(url):
    pageSource = test(url)
    pageSource = str(pageSource.text)
    # print(pageSource)
    print(check(pageSource, 'data-marker="item-view/title-info">', '</span>'))  # 3-к. квартира, 73,9м², 1/5эт.
    buff_str = check(pageSource, 'class="params-paramsList-zLpAu"',
                     '</ul>')  # отдельно сохраняю словарь с параметраии
    list1 = {'Количество комнат:': 0,
             'Общая площадь:': 0,
             'Площадь кухни:': 0,
             'Жилая площадь:': 0,
             'Этаж:': 0,
             'Тип комнат:': 0,
             'Высота потолков:': 0,
             'Санузел:': 0,
             'Окна:': 0,
             'Ремонт:': 0,
             'Способ продажи:': 0}

    list1_sub = ['Количество комнат:', 'Общая площадь:', 'Площадь кухни:', 'Жилая площадь:', 'Этаж:', 'Тип комнат:',
                 'Высота потолков:', 'Санузел:', 'Окна:', 'Ремонт:', 'Способ продажи:']

    for elem in list1_sub:  # парселинг отдельно списка с параметрами
        list1[elem] = check(buff_str, '</span>', '</li>')  # обращение к элементу словоря
        buff_str = buff_str[:buff_str.find('</span>')] + buff_str[buff_str.find('</li>') + 5:]

    return list1


x, y = get_rectangle_bounds([55.697965, 37.579133])
get_avito(x, y)