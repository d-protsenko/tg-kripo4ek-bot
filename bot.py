import config
import db_controller
import telebot
import logging
from pprint import pformat
import scheduler_utils
import scheduling

bot = telebot.TeleBot(config.token)
scheduler = scheduling.Scheduler()

money = {}


def start():
    bot.infinity_polling()


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(
        message.chat.id,
        'Привет, я крип, маленький такой крипочек. '
        '/creep'
    )


@bot.message_handler(commands=['midas'])
def midas(message):
    db_controller.upsert_creep_hp(message.chat.id, 0)
    money[message.chat.id] = money[message.chat.id] + 190
    bot.send_message(
        message.chat.id,
        'Вы замидасили своего крипа, теперь у него 0 хп. Зато у вас на счету теперь ' + str(money[message.chat.id])
    )


@bot.message_handler(commands=['creep'])
def creep(message):
    db_controller.upsert_creep_hp(message.chat.id, 100)
    degen_event = scheduler_utils.Event(
        'DEGEN',
        10,
        'degen_creep',
        {
            'chat_id': message.chat.id,
            'amount': 1
        }
    )
    scheduler.add_event(message.chat.id, degen_event)
    # TODO: if creep has 0 hp, create another one
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
    hp = db_controller.get_creep_hp(message.chat.id)
    if hp == 0:
        bot.send_message(message.chat.id, 'Для начала надо начать играть :^) /creep')
    else:
        bot.send_message(
            message.chat.id,
            'У твоего крипочка сейчас ' + str(hp) + ' здоровья'
        )


@bot.message_handler(commands=['feed'])
def feed(message):
    new_hp = db_controller.get_creep_hp(message.chat.id) + 5
    db_controller.upsert_creep_hp(message.chat.id, new_hp)
    bot.send_message(
        message.chat.id,
        'Твой крипочек успешно накормлен, теперь у него ' + str(new_hp) + ' здоровья'
    )


@bot.message_handler(content_types=['text'], regexp='push me to the edge')
def echo_message_easter_push(message):
    logging.debug(pformat(message))
    bot.send_message(message.chat.id, 'all the creeps are dead')


@bot.message_handler(content_types=['text'])
def echo_message(message):
    logging.debug(pformat(message))
    bot.send_message(message.chat.id, message.text)
