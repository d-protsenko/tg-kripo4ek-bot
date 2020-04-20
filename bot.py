import config
import telebot
import logging
from pprint import pformat
import scheduler_utils
import scheduling
import creep
import profile

bot = telebot.TeleBot(config.token)
scheduler = scheduling.Scheduler()


def start():
    bot.infinity_polling()


def authenticate(message):
    if profile.get_money(message.chat.id) == -1 or creep.get_creep_hp(message.chat.id) == -1:
        bot.send_message(
            message.chat.id,
            'Для начала нужно начать играть, используй /start'
        )
        return False
    return True


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    creep.set_creep_hp(message.chat.id, 100)
    profile.set_money(message.chat.id, 0)
    bot.send_message(
        message.chat.id,
        'Привет, я крип, маленький такой крипочек. '
        '/creep'
    )
    degen_event = scheduler_utils.Event(
        'DEGEN',
        30,
        'degen_creep',
        {
            'chat_id': message.chat.id,
            'amount': 1
        }
    )
    scheduler.add_event(message.chat.id, degen_event)


@bot.message_handler(commands=['midas'])
def midas(message):
    if not authenticate(message):
        return
    creep.set_creep_hp(message.chat.id, 0)
    profile.add_money(message.chat.id, 190)
    bot.send_message(
        message.chat.id,
        'Вы замидасили своего крипа, теперь у него 0 хп. Зато у вас на счету теперь ' +
        str(profile.get_money(message.chat.id))
    )


@bot.message_handler(commands=['creep'])
def create_creep(message):
    if not authenticate(message):
        return
    # TODO: if creep has 0 hp, create another one
    if creep.get_creep_hp(message.chat.id) == 0:
        creep.set_creep_hp(message.chat.id, 100)
        bot.send_message(
            message.chat.id,
            'Ты только что создал нового крипочка и у него сейчас 100 здоровья.'
        )
    else:
        bot.send_message(
            message.chat.id,
            'Сейчас у твоего крипочка ' + str(creep.get_creep_hp(message.chat.id)) + ' здоровья ' +
            '(используй /status, чтобы узнать сколько здоровья у твоего крипочка),' +
            ' и, пока что, они не убавляются,' +
            ' но ты можешь его покормить (используй /feed)' +
            ' и добавить ему немножко здоровья :^)'
        )


@bot.message_handler(commands=['status'])
def status(message):
    if not authenticate(message):
        return
    bot.send_message(
        message.chat.id,
        'У твоего крипочка сейчас ' + str(creep.get_creep_hp(message.chat.id)) + ' здоровья.\n' +
        'А у тебя ' + str(profile.get_money(message.chat.id)) + ' золота.'
    )


@bot.message_handler(commands=['feed'])
def feed(message):
    if not authenticate(message):
        return
    new_hp = creep.get_creep_hp(message.chat.id) + 5
    creep.set_creep_hp(message.chat.id, new_hp)
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
