from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "mvideo_parser"
MONGO_COLLECTION = "mvideo_parser_collection"


def mongo_delete():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        data = db[MONGO_COLLECTION]
        data.delete_many({})


del_hh_mongo = mongo_delete()