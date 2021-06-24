#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import requests
import os

def get_token():
    f = open("../Lesson1/github_token.txt", "r")
    token = f.readline().rstrip('\n')
    f.close()
    return token

def get_user_agent():
    f = open("../Lesson1/user-agent.txt", "r")
    user_agent = f.readline().rstrip('\n')
    f.close()
    return user_agent


username = 'MajeroRuf'

token = get_token()

repos = requests.get('https://api.github.com/user/repos', auth=(username, token), verify=False)

