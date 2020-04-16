import redis
import config
import logging
import scheduler_utils

cache = redis.Redis(host='localhost', port=6379, password=config.db_pwd)
event_postfix = "_EVENT"


def get_creep_hp(chat_id):
    return int(cache.get(chat_id))


def kill_creep(chat_id):
    cache.delete(chat_id)


def degen_creep(chat_id, amount):
    logging.debug("degen " + str(chat_id) + " on " + str(amount) + "hp")
    cache.decr(chat_id, int(amount))


def upsert_creep_hp(chat_id, hp):
    cache.set(chat_id, int(hp))


def save_event_to_db(id: str, event: scheduler_utils.Event):
    cache.hset(str(event.name + event_postfix), id, event.toJSON())


def load_event_from_db(id: str, event_name: str):
    return scheduler_utils.Event(
        json_string=scheduler_utils.decode_bytes(cache.hget(str(event_name + event_postfix), id))
    )


def load_all_events_from_db(event_name):
    all_events = cache.hgetall(event_name + event_postfix)
    event_list = []
    for k, v in all_events.items():
        event_list.append(
            scheduler_utils.Event(json_string=scheduler_utils.decode_bytes(v))
        )
    return event_list
