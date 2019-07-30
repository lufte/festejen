#!/usr/bin/env python3
import pickle
import os
from parser import generator
from telegram.ext import *


def handler(bot, update):
    try:
        message = generator.build(index, seed=update.message.text)
    except Exception as e:
        message = str(e)
    bot.sendMessage(update.message.chat_id, text=message)


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__),
                           'index.pickle'), 'rb') as f:
        index = pickle.load(f)
    with open(os.path.join(os.path.dirname(__file__),
                           'telegram-token')) as f:
        token = f.read().strip()

    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text | Filters.command, handler))
    updater.start_polling()
    updater.idle()
