import multiprocessing
import datetime
import time
import os

import tinydb
import telebot
from telebot import types
from config import config

if not os.path.exists(config['DB_PATH']):
    os.makedirs(os.path.dirname(config['DB_PATH']), exist_ok=True)

db = tinydb.TinyDB(config['DB_PATH'])
parent_query = tinydb.Query()

bot = telebot.TeleBot(config['BOT']['TOKEN'])


def is_business_day(date):
    return date.weekday() < 5


def execute_at(wake_time: datetime.time, callback, only_business, args=(), kwargs={}):
    while True:
        now = datetime.datetime.now()

        if only_business and not is_business_day(now):
            continue

        if now.hour == wake_time.hour \
                and now.minute == wake_time.minute \
                and now.second == wake_time.second:
            time.sleep(1)  # without delay it triggers many times a second
            callback(*args, **kwargs)


def get_food_orders():
    for parent in db.all():
        kb = generate_order_keyboard(parent['telegram_id'])

        bot.send_message(parent['telegram_id'],
                         config['BOT']['ASK_MESSAGE'],
                         reply_markup=kb)


def send_food_orders():
    parents_str = '\n'.join([parent['name']
                             for parent in db if parent.get('order_food', True)])

    send_to_admins('Їжу замовляють:\n' + parents_str)


def send_to_admins(message_text, args=(), kwargs={}):
    for admin in config['ADMINS']:
        bot.send_message(admin, message_text, *args, **kwargs)


def generate_order_keyboard(parent_id):
    keyboard_options = types.InlineKeyboardMarkup(row_width=2)
    keyboard_options.add(types.InlineKeyboardButton(
        text='Так!', callback_data=f'{parent_id}.1'))
    keyboard_options.add(types.InlineKeyboardButton(
        text='Ні...', callback_data=f'{parent_id}.0'))

    return keyboard_options


get_data_process = multiprocessing.Process(
    target=execute_at, args=(config['ASK_TIME'], get_food_orders, True))
send_data_process = multiprocessing.Process(
    target=execute_at, args=(config['SEND_TIME'], send_food_orders, True))


@bot.message_handler(commands=['start', 'help'])
def start_menu(message: telebot.types.Message):
    bot.reply_to(message, config['BOT']['START_MESSAGE'])
    u = message.chat

    if str(u.id) not in [parent['telegram_id'] for parent in db] and str(u.id) not in config['ADMINS']:
        add_parent_keyboard = types.InlineKeyboardMarkup(row_width=1)
        add_parent_keyboard.add(
            types.InlineKeyboardButton(text='Add to database', callback_data=f'{u.id}:{u.first_name} {u.last_name}'))

        send_to_admins(
            f'New user: {u.id}, {u.username}, {u.first_name}, {u.last_name}',
            kwargs={'reply_markup': add_parent_keyboard})


@bot.callback_query_handler(func=lambda call: True)
def inline_button(callback):
    data = callback.data

    if '.' in data:
        p_id, order = data.split('.')

        db.update({'order_food': True if order == '1' else False},
                  parent_query.telegram_id == p_id)
        bot.send_message(callback.from_user.id, config['BOT']['ACCEPTED'])

    elif ':' in data:
        p_id, p_name = data.split(':')
        db.insert({'telegram_id': p_id, 'name': p_name})
        bot.send_message(p_id, config['BOT']['ADDED'])


if __name__ == '__main__':
    get_data_process.start()
    send_data_process.start()

    bot.polling(none_stop=True)
