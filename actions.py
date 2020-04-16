import logging
import db_controller


def degen_creep(arguments: {}):
    logging.debug("degen " + str(arguments['chat_id']) + " on " + str(arguments['amount']) + "hp")
    db_controller.cache.decr(arguments['chat_id'], int(arguments['amount']))
