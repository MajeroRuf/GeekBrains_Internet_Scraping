"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД."""
"""3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта."""

from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup as bs
import re


MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancy"
MONGO_COLLECTION = "hh_vacancy_collection"


def mongo_record(hh_infos):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        data.insert_many(hh_infos)


def mongo_find_update(hh_infos):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        update_data = {}
        for item in hh_infos:
            filter_data = {}
            for key in item:
                filter_data[key] = {'$eq': item[key]}
            update_data['$set'] = item
            data.update_one(filter_data, update_data, upsert=True)

def get(url, headers, params, proxies):
    r = requests.get(
        url,
        headers=headers,
        params=params,
        proxies=proxies
    )
    return r


def len_pages():
    page = 0
    next_buttom = 0
    url1 = "https://hh.ru/search/vacancy"
    headers1 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"}
    proxies1 = {'http': 'http://202.169.252.102:8181'}

    while next_buttom is not None:
        params1 = {'text': vacancy, 'items_on_page': 50, 'page': page}
        p = requests.get(
            url1,
            headers=headers1,
            params=params1,
            proxies=proxies1
        )
        soup1 = bs(p.text, features="html.parser")
        next_buttom = soup1.find("a", {"class": "bloko-button", 'data-qa': 'pager-next'})
        page += 1
    return page


def parse_vacancies_on_page(vacancy, page):
    all_vacancies = []
    url = "https://hh.ru/search/vacancy"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"}
    proxies = {'http': 'http://202.169.252.102:8181'}

    params = {'text': vacancy, 'items_on_page': 50, 'page': page}
    r = requests.get(
        url,
        headers=headers,
        params=params,
        proxies=proxies
    )
    soup = bs(r.text, features="html.parser")
    vacancies_on_page = soup.find_all("div", {"class": "vacancy-serp-item"})

    # Списки с предварительными данными на этой странице
    vacancy_names = []
    vacancy_cities = []
    vacancy_hh_ids = []
    vacancy_links = []
    vacancy_site_name = []
    vacancy_salary_min = []
    vacancy_salary_max = []
    vacancy_company_names = []
    vacancy_company_links = []
    vacancy_responsibilities = []
    vacancy_requirements = []
    vacancy_dates = []
    vacancy_salary_in = []

    for vacancy in vacancies_on_page:
        vacancy_info_text = vacancy.find("div", {"class": "vacancy-serp-item__info"})

        # Название вакансии
        name_block = vacancy_info_text.find("a", {"class": "bloko-link"})
        if name_block is not None:
            name = name_block.text
        else:
            name = ""
        vacancy_names.append(name)

        # Ссылка на вакансию
        vacancy_link_block = vacancy_info_text.find("a", {"class": "bloko-link"})
        if vacancy_link_block is not None:
            vacancy_link = vacancy_link_block.get("href")
        else:
            vacancy_link = ""
        vacancy_links.append(vacancy_link)

        # Id вакансии на сайте hh
        if len(vacancy_link) == 0:
            vacancy_hh_id = None
        else:
            try:
                vacancy_hh_id = vacancy_link.split('/')[4].split("?")[0]
            except IndexError:
                vacancy_hh_id = None

        vacancy_hh_ids.append(vacancy_hh_id)

        # название сайта
        if len(vacancy_link) == 0:
            vacancy_site = None
        else:
            try:
                vacancy_site = vacancy_link.split('/')[2].split("/")[0]
            except IndexError:
                vacancy_site = None

        vacancy_site_name.append(vacancy_site)

        vacancy_salary_block = vacancy.find("div", {"class": "vacancy-serp-item__sidebar"})
        if vacancy_salary_block is not None:
            vacancy_salary = vacancy_salary_block.text
        else:
            vacancy_salary = ""

        # Заполнение зарплатных данных (может быть Null)
        if len(vacancy_salary) == 0:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(None)
        elif vacancy_salary.find("-") != -1:
            vacancy_salary_min.append(int(
                re.sub(r"\s+", "", vacancy_salary.split('-')[0].strip())))
            vacancy_salary_max.append(int(
                re.sub(r"\s+", "",
                       vacancy_salary.split('-')[1].split("руб")[0].split("USD")[0].split("EUR")[0].strip())))

        elif vacancy_salary.find("от") != -1:
            vacancy_salary_min.append(int(
                re.sub(r"\s+", "",
                       vacancy_salary.split('от')[1].split("руб")[0].split("USD")[0].split("EUR")[0].strip())))
            vacancy_salary_max.append(None)
        elif vacancy_salary.find("до") != -1:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(int(
                re.sub(r"\s+", "",
                       vacancy_salary.split('до')[1].split("руб")[0].split("USD")[0].split("EUR")[0].strip())))
        else:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(None)

        # В какой валюте зарплата (может быть Null)
        if vacancy_salary.find("руб") != -1:
            vacancy_salary_in.append("руб")
        elif vacancy_salary.find("USD") != -1:
            vacancy_salary_in.append("USD")
        elif vacancy_salary.find("EUR") != -1:
            vacancy_salary_in.append("EUR")
        else:
            vacancy_salary_in.append(None)

        # Название компании
        vacancy_company = vacancy.find("div", {"class": "vacancy-serp-item__meta-info"})
        if vacancy_company is not None:
            vacancy_company_name = vacancy_company.text.replace(u'\xa0', u'')
        else:
            vacancy_company_name = ""
        vacancy_company_names.append(vacancy_company_name)

        # Ссылка на компанию
        vacancy_company_link_block = vacancy_company.find("a", {"class": "bloko-link bloko-link_secondary"})
        if vacancy_company_link_block is not None:
            vacancy_company_link = "https://hh.ru" + vacancy_company_link_block.get('href')
        else:
            vacancy_company_link = ""
        vacancy_company_links.append(vacancy_company_link)

        # Город вакансии
        vacancy_city_block = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-address"})
        if vacancy_city_block is not None:
            vacancy_city = vacancy_city_block.text.split(',')[0]
        else:
            vacancy_city = ""
        vacancy_cities.append(vacancy_city)

        # Ответсвенность работника по данной вакансии
        vacancy_responsibility_block = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_responsibility"})
        if vacancy_responsibility_block is not None:
            vacancy_responsibility = vacancy_responsibility_block.text
        else:
            vacancy_responsibility = ""
        vacancy_responsibilities.append(vacancy_responsibility)

        # Требования для работника по данной вакансии
        vacancy_requirement_block = vacancy.find("div", {"data-qa": "vacancy-serp__vacancy_snippet_requirement"})
        if vacancy_requirement_block is not None:
            vacancy_requirement = vacancy_requirement_block.text
        else:
            vacancy_requirement = ""
        vacancy_requirements.append(vacancy_requirement)

        # Дата, когда была выложена вакансия
        vacancy_date_block = vacancy.find("span", {"class": "vacancy-serp-item__publication-date"})
        if vacancy_date_block is not None:
            vacancy_date_text = vacancy_date_block.text
        else:
            vacancy_date_text = ""

        if len(vacancy_date_text) == 0:
            vacancy_dates.append(None)
        else:
            vacancy_dates.append(vacancy_date_text)

    # Заполнение словарей по каждой вакансии
    for i in range(len(vacancy_names)):
        vacancy = {"name": vacancy_names[i],
                   "salary_from": vacancy_salary_min[i], "salary_to": vacancy_salary_max[i],
                   "salary_in": vacancy_salary_in[i],
                   "company_name": vacancy_company_names[i],
                   "date": vacancy_dates[i], "city": vacancy_cities[i], "hh_id": vacancy_hh_ids[i],
                   "vacancy_site": vacancy_site_name[i],
                   "responsibility": vacancy_responsibilities[i], "requirement": vacancy_requirements[i],
                   "link": vacancy_links[i], "link_to_company": vacancy_company_links[i]}
        all_vacancies.append(vacancy)
    return all_vacancies


vacancy = input("Введите вакансию: ")

page_all = len_pages()
number_page = int(input(f'По вашему запросу найдено {page_all} листов вакансии, '
                        f'напишите число листов для загрузки: '))
if number_page > page_all:
    print('Выбраное число листов превышает максимальное, будет выгружен только первый лист: ')
    number_page = 0

page = 0
while page <= number_page:
    hh_infos = parse_vacancies_on_page(vacancy, page)
    # vacancy_record = mongo_record(hh_infos)
    vacancy_record = mongo_find_update(hh_infos)
    page += 1
