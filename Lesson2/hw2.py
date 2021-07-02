"""Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность)
с сайтов Superjob(по желанию) и HH(обязательно).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
"""

import pickle
import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd

vacancy = input("Введите вакансию: ")

url = "https://hh.ru/search/vacancy"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218"}
proxies = {'http': 'http://202.169.252.102:8181'}
path = "hh.rsp"


def save_pickle(o, path):
    with open(path, 'wb') as f:
        pickle.dump(o, f)


def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


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
        params1 = {'text': vacancy, 'page': page}
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


def parse_vacancies_on_page():
    all_vacancies = []
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
            vacancy_salary_min.append(vacancy_salary.split('-')[0].encode('ascii', 'ignore'))
            vacancy_salary_max.append(
                vacancy_salary.split('-')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
        elif vacancy_salary.find("от") != -1:
            vacancy_salary_min.append(
                vacancy_salary.split('от')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
            vacancy_salary_max.append(None)
        elif vacancy_salary.find("до") != -1:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(
                vacancy_salary.split('до')[1].split("руб")[0].split("USD")[0].encode('ascii', 'ignore'))
        else:
            vacancy_salary_min.append(None)
            vacancy_salary_max.append(None)

        # В какой валюте зарплата (может быть Null)
        if vacancy_salary.find("руб") != -1:
            vacancy_salary_in.append("руб")
        elif vacancy_salary.find("USD") != -1:
            vacancy_salary_in.append("USD")
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


page_all = len_pages()
number_page = int(input(f'По вашему запросу найдено {page_all} листов вакансии, '
                        f'напишите число листов для загрузки: '))
if number_page > page_all:
    print('Выбраное число листов превышает максимальное, будет выгружен только первый лист: ')
    number_page = 0

page_p = 0

with open('data_hh.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)

while page_p < page_all:
    params = {'text': vacancy, 'page': page_p}
    r = get(url, headers, params, proxies)
    save_pickle(r, path)
    page_p += 1
    r = load_pickle(path)
    parse_vacancies_on_page().append(parse_vacancies_on_page())
    data = parse_vacancies_on_page()
    with open('data_hh.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data[0].keys())
        for dict_item in data:
            csv_writer.writerow(dict_item.values())

hh_df = pd.read_csv('data_hh.csv', encoding='cp1251')
print(hh_df)
