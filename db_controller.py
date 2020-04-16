import redis
import config
import logging

cache = redis.Redis(host='localhost', port=6379, password=config.db_pwd)


def get_creep_hp(chat_id):
    return int(cache.get(chat_id))


def kill_creep(chat_id):
    cache.delete(chat_id)


def degen_creep(chat_id, amount):
    logging.debug("degen " + str(chat_id) + " on " + str(amount) + "hp")
    cache.decr(chat_id, int(amount))


def upsert_creep_hp(chat_id, hp):
    cache.set(chat_id, int(hp))
