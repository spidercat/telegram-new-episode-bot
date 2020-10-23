import config
from db import Db
from pendingShows import get_shows, get_next_episode_number, prepare_next_episode

import os
import telegram
import logging
from datetime import datetime, time, timedelta
from telegram.ext import Updater
from telegram.ext import CommandHandler, Filters, MessageHandler, RegexHandler
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from collections import OrderedDict
from threading import Timer
db=Db()
bot = telegram.bot.Bot(config.TOKEN)
for i in db.get_quorum():
#     bot.send_message(i, "Плохой папа увез меня из дома \u1F621, но я вернулся!!!")
    emoji = b'\xF0\x9F\x98\xA1'.decode("utf-8", "replace")
    bot.send_message(i, f'Плохой папа увез меня из дома {emoji}, но я вернулся!!!' )

# bot.send_animation('898147660', 'https://media.giphy.com/media/6BZaFXBVPBtok/giphy.gif')
# bot.send_sticker('898147660', 'https://media.giphy.com/media/abonYnUKXMFLa/giphy.gif')
# bot.send_message('898147660', emoji)
# bot.send_message('898147660', 'Но я вернулся' )
# bot.send_message('898147660', emoji)
