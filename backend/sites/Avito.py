import undetected_chromedriver as uc
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
    driver = uc.Chrome()
    try:
        r = test(url, data).json()
        avito_urls = ['https://www.avito.ru' + elem['urlPath'] for elem in r['items']]
        for elem in avito_urls:
            print(elem, get_flat_params(elem, driver).get('Количество комнат:'))
    except Exception as exception:
        print(exception)


def check(pageSource, start_str, end_str):
    start = pageSource.find(start_str)
    end = pageSource.find(end_str, start)
    pageSource = pageSource[start + len(start_str):end].replace('&nbsp;', '').replace('\xa0', ' ')
    return pageSource


def get_flat_params(url, driver):
    pageSource = test(url, driver=driver)
    # print(pageSource)
    print(check(pageSource, 'data-marker="item-view/title-info">', '</span>'))  # 3-к. квартира, 73,9м², 1/5эт.

    list1 = {}

    list1_sub = ['Количество комнат:', 'Общая площадь:', 'Площадь кухни:', 'Жилая площадь:', 'Этаж:', 'Тип комнат:',
                 'Высота потолков:', 'Санузел:', 'Окна:', 'Ремонт:', 'Способ продажи:']

    list2_sub = ['Тип дома:', 'Год постройки:', 'Этажей в дома:', 'Пассажирский лифт:']

    buff_str = check(pageSource, 'class="params-paramsList-zLpAu"',
                     '</ul>')  # отдельно сохраняю словарь с параметраии

    for elem in list1_sub:  # парселинг отдельно списка с параметрами(list1_sub)
        list1[elem] = check(buff_str, '</span>', '</li>')  # обращение к элементу словоря
        buff_str = buff_str[:buff_str.find('</span>')] + buff_str[buff_str.find('</li>') + 5:]

    buff_str = check(pageSource, 'class="style-item-params-list-vb1_H"',
                     '</ul>')  # отдельно сохраняю второй список с параметраии

    for elem in list2_sub:  # парселинг отдельно списка с параметрами(list2_sub)
        list1[elem] = check(buff_str, '</span>', '</li>')
        buff_str = buff_str[:buff_str.find('</span>')] + buff_str[buff_str.find('</li>') + 5:]

    return list1


if __name__ == '__main__':

    x, y = get_rectangle_bounds([55.697965, 37.579133])
    # get_avito(x, y)
    print(x, y)
