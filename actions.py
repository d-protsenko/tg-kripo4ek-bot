import logging
import creep


def degen_creep(arguments: {}):
    if creep.get_creep_hp(arguments['chat_id']) - int(arguments['amount']) > 0:
        logging.debug("degen " + str(arguments['chat_id']) + " creep on " + str(arguments['amount']) + "hp")
        creep.degen_creep(arguments['chat_id'], int(arguments['amount']))
    else:
        logging.debug("creep " + str(arguments['chat_id']) + " died")
        creep.set_creep_hp(arguments['chat_id'], 0)
