"""2. Написать функцию, которая производит поиск и выводит на экран вакансии
 с заработной платой больше введённой суммы."""

from pymongo import MongoClient
from pprint import pprint

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "hh_vacancy"
MONGO_COLLECTION = "hh_vacancy_collection"


def mongo_find():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        cursor = data.find({"salary_from": {"$gt": salary}})
    return cursor


salary = int(input('Введите желаемую з/п: '))

for doc in mongo_find():
    pprint(doc)
