import pymongo
import config

client = pymongo.MongoClient('localhost', 27017)
db = client[config.db_name]
db.authenticate(config.db_user, config.db_user_pwd)


def create_collection(name):
    db.create_collection(name)


def add_new_creep(chat_id, hp):
    db.get_collection('creep').insert_one({'chat_id': chat_id, 'hp': hp})
