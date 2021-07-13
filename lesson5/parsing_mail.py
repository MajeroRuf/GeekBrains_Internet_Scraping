"""Написать программу, которая собирает входящие письма из своего
или тестового почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
import time

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mail_parser"
MONGO_COLLECTION = "mail_parser_collection"

def mongo_find_update(news_infos):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        update_data = {}
        for item in news_infos:
            filter_data = {}
            for key in item:
                filter_data[key] = {'$eq': item[key]}
            update_data['$set'] = item
            data.update_one(filter_data, update_data, upsert=True)


chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

elem = driver.find_element_by_css_selector('input[class="email-input svelte-1eyrl7y"]')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

elem = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.NAME, 'password')))
elem.send_keys('NextPassword172!')
elem.send_keys(Keys.ENTER)


link_all = set()
time.sleep(3)
email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
link_list = list(map(lambda el: el.get_attribute('href'), email_list))
link_all = link_all.union(set(link_list))

while True:
    actions = ActionChains(driver)
    actions.move_to_element(email_list[-1])
    actions.perform()

    time.sleep(3)
    email_list = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    link_list = list(map(lambda el: el.get_attribute('href'), email_list))

    if link_list[-1] not in link_all:
        link_all = link_all.union(set(link_list))
        continue
    else:
        break

new_mail_list =[]
for href in list(link_all):
    driver.get(href)
    new_mail = {}
    time.sleep(3)
    new_mail['text'] = driver.find_element_by_class_name('letter-body').text
    new_mail['sender'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
    new_mail['title'] = driver.find_element_by_xpath('//h2').text
    new_mail['data'] = driver.find_element_by_class_name('letter__date').text
    new_mail_list.append(new_mail)

goods_record = mongo_find_update(new_mail_list)

driver.quit()