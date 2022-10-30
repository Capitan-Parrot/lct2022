import undetected_chromedriver as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://www.avito.ru/moskva/kvartiry/3-k._kvartira_739m_15et._2411657289")
pageSource = driver.page_source
pageSource=str(pageSource)
# print(pageSource)


print(cheak(pageSource,'data-marker="item-view/title-info">','</span>'))#3-к. квартира, 73,9м², 1/5эт.

buff_str=cheak2(pageSource)
print(buff_str)
for i in range(10):
    print(cheak(buff_str,'</span>','</li>'))
    buff_str.replace('</span>','',1)
    buff_str.replace('</li>','', 1)


