import json
from pprint import pprint

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
driver = uc.Chrome(use_subprocess=True)
url = 'https://www.avito.ru/js/1/map/items?categoryId=24&locationId=637640&correctorMode=0&page=1&map=eyJzZWFyY2hBcmVhIjp7ImxhdEJvdHRvbSI6NTYuMDY4NDc0MDc5MTg3OTgsImxhdFRvcCI6NTYuMTU2OTExNjY3MTE4MDEsImxvbkxlZnQiOjQwLjE3MDY3MDQzOTA0NjQxLCJsb25SaWdodCI6NDAuNDM4NDYyMTg3MDkzMjg2fSwiem9vbSI6MTJ9&params%5B201%5D=1059&verticalCategoryId=1&rootCategoryId=4&localPriority=0&searchArea%5BlatBottom%5D=77.07847407918798&searchArea%5BlonLeft%5D=90.17067043904641&searchArea%5BlatTop%5D=56.15691166711801&searchArea%5BlonRight%5D=40.438462187093286&viewPort%5Bwidth%5D=780&viewPort%5Bheight%5D=462&limit=10&countAndItemsOnly=1'
driver.get(url)
content = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "pre")))
data = json.loads(content.text)["items"]
pprint(content.text)