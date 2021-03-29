import secrets
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

updater = Updater(secrets.TOKEN)
dispatcher = updater.dispatcher
db = Db()

workday_start = time(7,0)
workday_end = time(20,0)
def is_working_hours():
    now = datetime.now().time()
    return now >= workday_start and now <= workday_end

cool_down_interval = 30

pending_request_timeout = 150.0

daily_limit = 3

timeout_timer = Timer(2.0, lambda: print('hi'))

copied_today_count = 0
last_copied_episode = datetime.now() - timedelta(days=7) # just a date in a not so recent past
pending_episode = {}

def handle_unsupported_user(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    print(f'username: {update.message.chat.username}')
    print(f'first_name: {update.message.chat.first_name}')
    print(f'last_name: {update.message.chat.last_name}')
    print(f'chat id : {chat_id}')
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    time.sleep(2)
    bot.send_message(chat_id, "Я обслуживаю только очень узкий круг ограниченных людей. Вы не из их числа.")

def start(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id

    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

def message(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

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
    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    def send_disclaimer():
        update.message.reply_text("It might take a few moments ...")
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    t = Timer(1.0, send_disclaimer)
    t.start()
    common_shows = "\n".join(get_shows())
    private_shows = "\n".join(get_shows(db.get_name(chat_id)))
    if private_shows == '':
        shows = common_shows
    else:
        shows = f"- Common shows -\n\n{common_shows}\n\n- Your private shows -\n\n{private_shows}"

    t.cancel()
    update.message.reply_text(shows)

def please(bot: telegram.bot.Bot, update: telegram.update.Update, args):
    chat_id = update.message.chat.id
    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

    if not is_working_hours():
        bot.send_message(chat_id, f"Leave me alone. I don't handle requests outside of working hours ({workday_start.strftime('%H:%M')} - {workday_end.strftime('%H:%M')}).")
        return

    remove_keyboard = ReplyKeyboardRemove()

    global pending_episode
    global last_copied_episode
    global cool_down_interval
    global pending_request_timeout
    global timeout_timer
    global daily_limit
    global copied_today_count

    show = ' '.join(args)
    if show in get_shows(db.get_name(chat_id)):
        copy_private_episode(bot, show, chat_id)
        return
    elif show not in get_shows():
        bot.send_message(chat_id, f"There is no such show '{show}'. Try /shows to see the list of available ones.", reply_markup=remove_keyboard)
        return

    if last_copied_episode + timedelta(minutes=cool_down_interval) > datetime.now():
        bot.send_message(chat_id, f"Patience, my friend. Only {(datetime.now() - last_copied_episode).seconds//60} minutes passed since last time", reply_markup=remove_keyboard)
        return

    if pending_episode:
        bot.send_message(chat_id, f"First finish with {pending_episode['name']}'s request for {pending_episode['show']}", reply_markup=remove_keyboard)
        return

    now = datetime.now()
    today_work_start = datetime(now.year, now.month, now.day, workday_start.hour, workday_start.minute)
    if last_copied_episode < today_work_start:
        print(f"now: {now}")
        print(f"today_work_start: {today_work_start}")
        print(f"last_copied_episode: {last_copied_episode}")

        copied_today_count = 0

    if copied_today_count >= daily_limit:
        bot.send_message(chat_id, f"You had {daily_limit} new episodes today already. Go do some pushups instead ;-)", reply_markup=remove_keyboard)
        return

    timeout_timer = Timer(pending_request_timeout, lambda: cancel(bot))
    timeout_timer.start()
    pending_episode['show'] = show
    pending_episode['name'] = db.get_name(chat_id)
    pending_episode['date'] = update.message.date
    pending_episode['aye'] = [chat_id]
    print(f"new episode request: {pending_episode}")

    for i in db.get_quorum([chat_id]):
        bot.send_message(i, f"{pending_episode['name']} wants another episode of '{show}' (/aye to accept, /nay to reject)", reply_markup=remove_keyboard)

    bot.send_message(chat_id, f"I'll ask them about '{show}'", reply_markup=remove_keyboard)

def is_quorum():
    global pending_episode
    # return not db.get_quorum(pending_episode['aye'])
    return len(pending_episode['aye']) > 1

def copy_episode(bot: telegram.bot.Bot):
    global pending_episode
    global last_copied_episode
    global copied_today_count

    show = pending_episode['show']
    episode_number = get_next_episode_number(show)

    for i in pending_episode['aye']:
        bot.send_message(i, f"Start copying new episode of '{show}': {' '.join(episode_number)}")

    error = prepare_next_episode(show)

    if not error:
        copied_today_count = copied_today_count + 1
        message = f"Copy #{copied_today_count} is complete"
        last_copied_episode = datetime.now()
    else:
        message = f"Copy failed with the following error: {error}"

    for i in pending_episode['aye']:
        bot.send_message(i, message)

    pending_episode = {}

def copy_private_episode(bot: telegram.bot.Bot, show, chat_it):
    # global last_copied_episode
    # global copied_today_count

    print(f"copy private episode for {db.get_name(chat_it)}")
    episode_number = get_next_episode_number(show, db.get_name(chat_it))

    print(f"{db.get_name(chat_it)} asked for {show}")
    bot.send_message(chat_it, f"Start copying new episode of '{show}': {' '.join(episode_number)}")

    time.sleep(2)
    bot.send_message(chat_it, f"Sorry, it's not fully working yet. [:-(")
    return

    error = prepare_next_episode(show, db.get_name(chat_it))

    if not error:
        # copied_today_count = copied_today_count + 1
        # message = f"Copy #{copied_today_count} is complete"
        # last_copied_episode = datetime.now()
        message = f"Copy is complete"
    else:
        message = f"Copy failed with the following error: {error}"

    bot.send_message(chat_it, message)

def aye(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

    global pending_episode

    if not pending_episode:
        update.message.reply_text(f"Hold your horses. There are no pending requests.")
        return

    if chat_id in pending_episode['aye']:
        update.message.reply_text(f"Darling, wait for the rest to respond.")
        return

    # notify
    pending_episode['aye'].append(chat_id)

    for i in db.get_quorum([chat_id]):
        # TODO: make better message
        bot.send_message(i, f"{db.get_name(chat_id)} says: Aye, Aye Captain!!")

    if is_quorum():
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        global timeout_timer
        timeout_timer.cancel()
        copy_episode(bot)

def nay(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    if not db.is_family(chat_id):
        handle_unsupported_user(bot, update)
        return

    global pending_episode
    global timeout_timer

    if not pending_episode:
        update.message.reply_text(f"Why so negative ? There are no pending requests.")
        return

    if chat_id in pending_episode['aye']:
        update.message.reply_text(f"Darling, you've said your piece already. No turning back on your word.")
        return

    pending_episode = {}
    timeout_timer.cancel()

    for i in db.get_quorum([chat_id]):
        # TODO: make better message
        bot.send_message(i, f"{db.get_name(chat_id)} says nay.  彡(-_-;)彡")

def cancel(bot: telegram.bot.Bot):
    global pending_episode
    for i in db.get_quorum():
        bot.send_message(i, f"{pending_episode['name']}'s request for '{pending_episode['show']}' expired.  (ɵ̥̥ ˑ̫ ɵ̥̥)")

    pending_episode = {}

def whoami(bot: telegram.bot.Bot, update: telegram.update.Update):
    chat_id = update.message.chat.id
    if not db.is_family(chat_id) and not db.is_guest(chat_id):
        handle_unsupported_user(bot, update)
        return

    me = db.whoami(chat_id)
    print(f"{chat_id}  /whoami:  {me}")
    update.message.reply_text(me)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('shows', shows))
dispatcher.add_handler(CommandHandler('please', please, pass_args=True))
dispatcher.add_handler(CommandHandler('aye', aye))
dispatcher.add_handler(CommandHandler('nay', nay))
dispatcher.add_handler(CommandHandler('whoami', whoami))
dispatcher.add_handler(MessageHandler(Filters.all, message, edited_updates=True))

updater.start_polling()
updater.idle()
