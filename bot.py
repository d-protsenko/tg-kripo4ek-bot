import config
import db_controller
import telebot
import logging
from pprint import pformat
import threading

bot = telebot.TeleBot(config.token)

creep_map = {}
money = {}


def add_to_map(chat_id, hp):
    creep_map[chat_id] = hp


def update_in_map(chat_id, hp):
    creep_map[chat_id] = hp


def get_creep_hp(chat_id):
    try:
        return creep_map[chat_id]
    except Exception as ex:
        return 0


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(
        message.chat.id,
        'Привет, я крип, маленький такой крипочек. '
        '/creep'
    )


@bot.message_handler(commands=['midas'])
def midas(message):
    creep_map[message.chat.id] = 0
    money[message.chat.id] = money[message.chat.id] + 190
    bot.send_message(
        message.chat.id,
        'Вы замидасили своего крипа, теперь у него 0 хп. Зато у вас на счету теперь ' + str(money[message.chat.id])
    )


@bot.message_handler(commands=['creep'])
def creep(message):
    db_controller.add_new_creep(message.chat.id, 100)
    # TODO: if creep has 0 hp, create another one
    add_to_map(message.chat.id, 100)
    money[message.chat.id] = 0
    bot.send_message(
        message.chat.id,
        'Сейчас у твоего крипочка 100 здоровья '
        '(используй /status, чтобы узнать сколько здоровья у твоего крипочка),'
        ' и, пока что, они не убавляются,'
        ' но ты можешь его покормить (используй /feed)'
        ' и добавить ему немножко здоровья :^)'
    )


@bot.message_handler(commands=['status'])
def status(message):
    hp = get_creep_hp(message.chat.id)
    if hp == 0:
        bot.send_message(message.chat.id, 'Для начала надо начать играть :^) /creep')
    else:
        bot.send_message(
            message.chat.id,
            'У твоего крипочка сейчас ' + str(get_creep_hp(message.chat.id)) + ' здоровья'
        )


@bot.message_handler(commands=['feed'])
def feed(message):
    new_hp = get_creep_hp(message.chat.id) + 5
    update_in_map(message.chat.id, new_hp)
    bot.send_message(
        message.chat.id,
        'Твой крипочек успешно накормлен, теперь у него ' + str(new_hp) + ' здоровья'
    )


@bot.message_handler(content_types=["text"], regexp='push me to the edge')
def echo_message_easter_push(message):
    logging.debug(pformat(message))
    bot.send_message(message.chat.id, 'all the creeps are dead')


@bot.message_handler(content_types=["text"])
def echo_message(message):
    logging.debug(pformat(message))
    bot.send_message(message.chat.id, message.text)


def hp_degen():
    for x in creep_map:
        if creep_map[x] > 0:
            creep_map[x] = creep_map[x] - 1


def create_scheduled_event(interval, action, actionargs=()):
    threading.Timer(interval, create_scheduled_event, (interval, action, actionargs)).start()
    action(*actionargs)


if __name__ == '__main__':
    db_controller.create_collection('creep')
    logging.getLogger().setLevel(logging.DEBUG)
    create_scheduled_event(10, hp_degen)
    bot.infinity_polling()
