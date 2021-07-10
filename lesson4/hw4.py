""" Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
Для парсинга использовать xpath. Структура данных должна содержать:
- название источника,
- наименование новости,
- ссылку на новость,
- дата публикации

Нельзя использовать BeautifulSoup"""

import requests
from pymongo import MongoClient
from lxml.html import fromstring
from datetime import datetime

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "news_parser"
MONGO_COLLECTION = "news_parser_collection"


def date_format(date):
    date_list = date.split('T')
    news_time = date_list[1].strip().split('+')[0]
    news_date = date_list[0].strip()
    date_time_str = f'{news_date} {news_time}'
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
    return date_time_obj

def parser_xpath_lenta():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    url = "https://lenta.ru"
    response = requests.get(url, headers=headers)

    lenta_xpath = '//section[contains(@class,"js-top-seven")]/div[contains(@class,"span4")][position()=2]/div[' \
                  'contains(@class,"item")]'

    dom = fromstring(response.text)
    lenta_items = dom.xpath(lenta_xpath)
    news_about_lenta = []
    for news in lenta_items:
        info_lenta = {}
        info_lenta["source"] = "lenta.ru"
        info_lenta["news_name"] = news.xpath("./a/text()")[0]
        info_lenta["news_url"] = "https://lenta.ru" + news.xpath("./a/@href")[0]
        info_lenta["news_date"] = news.xpath("./a/time/@datetime")[0]
        news_about_lenta.append(info_lenta)
    return news_about_lenta
print(parser_xpath_lenta())

def parser_xpath_yandex():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    url = "https://yandex.ru/news/"
    response = requests.get(url, headers=headers)

    yandex_xpath = "//div[contains(@class,'news-app__top')][position()=1]//div[contains(@class, 'mg-grid__col')]"

    dom = fromstring(response.text)
    yandex_items = dom.xpath(yandex_xpath)
    news_about_yandex = []
    for news in yandex_items:
        info_yandex = {}
        info_yandex["source"] = news.xpath("./article//a[contains(@class, 'mg-card__source-link')]/text()")[0]
        info_yandex["news_name"] = news.xpath("./article//a[contains(@class,'mg-card__link')]/h2/text()")[0]
        info_yandex["news_url"] = news.xpath("./article//a[contains(@class,'mg-card__link')]/@href")[0]
        info_yandex["news_date"] = news.xpath("./article//span[contains(@class, "
                                                          "'mg-card-source__time')]/text()")[0]
        news_about_yandex.append(info_yandex)
    return news_about_yandex
print(parser_xpath_yandex())


def parser_xpath_mail():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    url = "https://news.mail.ru"
    response = requests.get(url, headers=headers)

    mail_xpath = "//div[contains(@class,'js-topnews')]//div[contains(@class,'daynews__item')]"

    dom = fromstring(response.text)
    mail_items = dom.xpath(mail_xpath)
    news_about_mail = []
    for news in mail_items:
        info_mail = {}
        info_mail["source"] = 'news.mail.ru'
        info_mail["news_name"] = news.xpath("./a[contains(@class, 'js-topnews__item')]"
                                            "/span/span/text()")[0]
        info_mail["news_url"] = news.xpath("./a[contains(@class, 'js-topnews__item')]/@href")[0]
        info_mail["news_date"] = date_format(news.xpath("//span[contains(@class, 'js-ago')]/@datetime")[0])
        news_about_mail.append(info_mail)
    return news_about_mail
print(parser_xpath_mail())

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




news_infos = parser_xpath_lenta()
news_record = mongo_find_update(news_infos)
news_infos = parser_xpath_yandex()
news_record1 = mongo_find_update(news_infos)
news_infos = parser_xpath_mail()
news_record2 = mongo_find_update(news_infos)