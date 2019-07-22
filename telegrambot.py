#!/usr/bin/env python3
import pickle
import re
import os
from parser import generator
from telegram.ext import *


word_pattern = re.compile('\w+(?=\W*$)')
with open(os.path.join(os.path.dirname(__file__),
                       './index.pickle'), 'rb') as f:
    index = pickle.load(f)


def handler(bot, update):
    try:
        last_word = word_pattern.search(update.message.text).group(0)
        message = generator.build(index, start_word=last_word)
    except (KeyError, TypeError, AttributeError):
        message = generator.build(index)
    except Exception as e:
        message = str(e)
    bot.sendMessage(update.message.chat_id, text=message)


if __name__ == '__main__':
    updater = Updater('931610532:AAE1yn9-oonUg_E2wZBJRs7JnOXxOp6vvCk')
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handler))
    updater.start_polling()
    updater.idle()
