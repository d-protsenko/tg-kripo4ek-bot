import db_controller

money_hash = 'money'


def get_money(chat_id):
    if db_controller.exists(money_hash, chat_id):
        return int(db_controller.get(money_hash, chat_id))
    else:
        return -1


def set_money(chat_id, value):
    return db_controller.set(money_hash, chat_id, value)


def add_money(chat_id, amount):
    return db_controller.set(money_hash, chat_id, get_money(chat_id) + amount)
