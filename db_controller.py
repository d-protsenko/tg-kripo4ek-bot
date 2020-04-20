import redis
import config
import scheduler_utils

redis = redis.Redis(host='localhost', port=6379, password=config.db_pwd)
event_postfix = "_EVENT"


def plain_get(obj_id):
    return redis.get(obj_id)


def plain_set(obj_id, value):
    return redis.set(obj_id, value)


def plain_del(obj_id):
    return redis.delete(obj_id)


def plain_exist(obj_id):
    return not redis.exists(obj_id) == 0


def get(obj_hash, obj_id):
    return redis.hget(obj_hash, obj_id)


def set(obj_hash, obj_id, value):
    return redis.hset(obj_hash, obj_id, value)


def delete(obj_hash, obj_id):
    return redis.hdel(obj_hash, obj_id)


def incrby(obj_hash, obj_id, amount):
    return redis.hincrby(obj_hash, obj_id, amount)


def exists(obj_hash, obj_id):
    return redis.hexists(obj_hash, obj_id)


def save_event_to_db(obj_id: str, event: scheduler_utils.Event):
    if redis.exists(str(event.name + event_postfix)) == 0:
        redis.hset(str(event.name + event_postfix), obj_id, event.toJSON())
        return True
    return False


def load_event_from_db(obj_id: str, event_name: str):
    return scheduler_utils.Event(
        json_string=scheduler_utils.decode_bytes(redis.hget(str(event_name + event_postfix), obj_id))
    )


def load_all_events_from_db(event_name):
    all_events = redis.hgetall(event_name + event_postfix)
    event_list = []
    for k, v in all_events.items():
        event_list.append(
            scheduler_utils.Event(json_string=scheduler_utils.decode_bytes(v))
        )
    return event_list
