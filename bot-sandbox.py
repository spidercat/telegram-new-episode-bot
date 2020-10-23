import config

import os
import telegram
import logging
import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler, Filters, MessageHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
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
chat_id_to_attempt_count = {}

# 
def start(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    attempt_count = chat_id_to_attempt_count.get(chat_id, -1)

    if attempt_count == -1:
        print(f'username: {update.message.chat.username}')
        print(f'first_name: {update.message.chat.first_name}')
        print(f'last_name: {update.message.chat.last_name}')
        print(f'chat id : {chat_id}')
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Спасибо ;-)")
    elif attempt_count == 0:
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Ну чаво ???")
        time.sleep(1)
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Я только родился и ничего не умею.")
    elif attempt_count == 1:
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Я что, на тормоза попал?")
        time.sleep(1)
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Н О В Ы Й   Я.")
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(2)
        update.message.reply_text("Н И Ч Е Г О   Н Е   У М Е Ю ! ! !")
    else:
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        time.sleep(1)
        update.message.reply_text("отстань")
        

    chat_id_to_attempt_count[chat_id] = attempt_count + 1

    # title = update.message.text
    # title = title.replace("/start@"+BOT_NAME, "").strip()
    # title = title.replace("/start", "").strip()

    # text = pollText(poll)

    # reply_markup = poll_reply_markup(answers)
    # message = bot.sendMessage(chat_id=chat_id, text=text, reply_markup=reply_markup)

def message(bot: telegram.bot.Bot, update: telegram.update.Update):
    if update.message:
        print("New message arrived:")
        print(update.message)

    if update.edited_message:
        print(f"Message '{update.edited_message.text}' was edited")
        bot.send_message(update.edited_message.chat_id, "I don't read edited messages. If you want my attention, repost!", reply_to_message_id=update.edited_message.message_id)
    
    # print(update.message)
    print()

def shows(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id

    markup = ReplyKeyboardMarkup(keyboard=[['Time', InlineKeyboardButton(text='Logo', callback_data='1234567890')],["File", "Audio"]])
    bot.send_message (chat_id, "Hi! Which one do you want? choose from the below keyboard buttons.", reply_markup=markup)
    bot.send_message(chat_id, datetime.datetime.now().strftime("%H:%M:%S"))

start_handler = CommandHandler('start', start)
shows_handler = CommandHandler('shows', shows)
message_handler = MessageHandler(Filters.all, message, edited_updates=True)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(shows_handler)
dispatcher.add_handler(message_handler)
updater.start_polling()
updater.idle()
