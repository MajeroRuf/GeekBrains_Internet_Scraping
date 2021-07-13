from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "vacancies_hh_sj"
# MONGO_COLLECTION = "hhru"
MONGO_COLLECTION = "Superjobru"

def mongo_delete():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        data.delete_many({})


del_hh_mongo = mongo_delete()