"""Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
 Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from pymongo import MongoClient
import time

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mvideo_parser"
MONGO_COLLECTION = "mvideo_parser_collection"


def mongo_find_update(new_items):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        update_data = {}
        for item in new_items:
            filter_data = {}
            for key in item:
                filter_data[key] = {'$eq': item[key]}
            update_data['$set'] = item
            data.update_one(filter_data, update_data, upsert=True)

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru')

newsellers = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-block-id="Novinki"]')))

driver.execute_script('window.scrollTo(0, 1500)')
time.sleep(3)
while True:
    try:
        button = WebDriverWait(newsellers, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'i-icon-fl-arrow-right')))
        button.click()
    except exceptions.TimeoutException:
            print('except')
            break

goods = newsellers.find_elements_by_class_name('gallery-list-item')
new_items =[]
for good in goods:
    new_item = {}
    new_item['title'] = good.find_element_by_tag_name(
        'a').get_attribute('data-track-label')
    new_item['good_link'] = good.find_element_by_tag_name(
        'a').get_attribute('href')
    new_item['good_info'] = good.find_element_by_tag_name(
        'a').get_attribute('data-product-info')
    # new_items['price'] = good.find_element_by_class_name('fl-product-tile-price__current').text
    # new_items['img'] = good.find_element_by_tag_name('img').get_attribute('Src')
    new_items.append(new_item)


print(new_items)


goods_record = mongo_find_update(new_items)

driver.quit()