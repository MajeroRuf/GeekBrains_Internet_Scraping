"""Зарегистрироваться на https://openweathermap.org/api и написать функцию,
которая получает погоду в данный момент для города, название которого получается через input.
https://openweathermap.org/current"""

import requests


def get_token():
    f = open("../Lesson1/openweathermap_token.txt", "r")
    token = f.readline().rstrip('\n')
    f.close()
    return token


url = 'http://api.openweathermap.org'
city = input("Введите город: ")
city_id = 0
weather = {}


def get_city_id():
    global city_id
    try:
        res = requests.get(f'{url}/data/2.5/find',
                           params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': get_token()})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id =', city_id)
    except Exception as error:
        print("Exception (find):", error)
    return city_id


def get_weather():
    global weather
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': get_city_id(), 'units': 'metric', 'lang': 'ru', 'APPID': get_token()})
        data = res.json()
        description = data['weather'][0]['description']
        temp = data['main']['temp']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        weather = {'description': description, 'temp': temp, 'temp_min': temp_min,
                   'temp_max': temp_max}
        print("Условия:", description)
        print("Температура:", temp)
        print("Минимальная температура:", temp_min)
        print("Максимальная температура:", temp_max)
    except Exception as error:
        print("Exception (weather):", error)
    return weather


print(get_weather())
