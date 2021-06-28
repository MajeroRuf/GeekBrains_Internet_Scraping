"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
 сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

"""

import requests
import json


def get_user_repo():
    url = 'https://api.github.com'
    user = input("Введите Имя пользователя GitHub: ")
    repo = []

    r = requests.get(f'{url}/users/{user}/repos')

    with open('data.json', 'w') as f:
        json.dump(r.json(), f)

    for i in r.json():
        repo.append(i['name'])

    return repo
