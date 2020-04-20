import db_controller
import logging

creep_hash = 'creep'


def get_creep_hp(chat_id):
    if db_controller.exists(creep_hash, chat_id):
        return int(db_controller.get(creep_hash, chat_id))
    else:
        return -1


def kill_creep(chat_id):
    db_controller.delete(creep_hash, chat_id)


def degen_creep(chat_id, amount):
    db_controller.incrby(creep_hash, chat_id, -int(amount))


def set_creep_hp(chat_id, hp):
    db_controller.set(creep_hash, chat_id, int(hp))


def add_creep_hp(chat_id, amount):
    return db_controller.set(creep_hash, chat_id, get_creep_hp(chat_id) + amount)
