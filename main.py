import config

import os
import telegram
import logging
import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time
from collections import OrderedDict

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#HEROKU_URL = 'https://HEROKU-APP-NAME.herokuapp.com'

#PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(config.TOKEN)
dispatcher = updater.dispatcher

# add handlers
# updater.start_webhook(listen="0.0.0.0",
#                       port=PORT,
#                       url_path=TOKEN)

# updater.bot.set_webhook(HEROKU_URL + "/" + TOKEN)

# 
def start(bot, update):
    chat_id = update.message.chat.id

    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(2)
    update.message.reply_text("Ну чаво ???")
    time.sleep(1)
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(2)
    update.message.reply_text("Я только родился и ничего не умею.")

    # title = update.message.text
    # title = title.replace("/start@"+BOT_NAME, "").strip()
    # title = title.replace("/start", "").strip()

    # text = pollText(poll)

    # reply_markup = poll_reply_markup(answers)
    # message = bot.sendMessage(chat_id=chat_id, text=text, reply_markup=reply_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
updater.idle()
