import datetime
import multiprocessing
import os
import time
import logging
from collections import Counter

import telebot
import tinydb
from telebot import types

from config import config

if not os.path.exists(config['DB_PATH']):
    os.makedirs(os.path.dirname(config['DB_PATH']), exist_ok=True)

db = tinydb.TinyDB(config['DB_PATH'])
user_query = tinydb.Query()

bot = telebot.TeleBot(config['BOT']['TOKEN'])

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logging.basicConfig(filename=config['LOG_PATH'],
                    format=config['LOG_FORMAT'],
                    level=logging.DEBUG)


def is_admin(u_id):
    return str(u_id) in config['ADMINS']


def is_user(u_id):
    return str(u_id) in [p['telegram_id'] for p in db]


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
            logging.info('Executing %s at %r', callback.__name__, wake_time)


def get_food_orders():
    for user in db:
        kb = generate_order_keyboard(user['telegram_id'])

        try:
            bot.send_message(user['telegram_id'],
                             config['BOT']['ASK_MESSAGE'],
                             reply_markup=kb)

            logging.info('Sent request to %s; id: %s',
                         user['name'], user['telegram_id'])

        except:
            logging.info('Unable to send message to %s; id: %s',
                         user['name'], user['telegram_id'])


def send_food_orders():
    send_to_admins(config['BOT']['ORDERS_LIST_TITLE'] +
                   generate_users_str(with_orders=True))

    logging.info('Sent list of orders to admins')


def send_to_admins(message_text, args=(), kwargs={}):
    for admin in config['ADMINS']:
        bot.send_message(admin, message_text, *args, **kwargs)

        logging.info('Sent message to admin (%s); message: %s',
                     admin, message_text)


def generate_order_keyboard(user_id):
    keyboard_options = types.InlineKeyboardMarkup(row_width=2)
    keyboard_options.add(types.InlineKeyboardButton(
        text=config['BOT']['KEYBOARDS']['YES'], callback_data=f'{user_id}.1'))
    keyboard_options.add(types.InlineKeyboardButton(
        text=config['BOT']['KEYBOARDS']['NO'], callback_data=f'{user_id}.0'))

    return keyboard_options


def generate_users_str(with_orders=False, with_ids=False):
    p_list = '\n'.join([((user['telegram_id'] + ' - ') if with_ids else '')
                        + user['name'] +
                        ((' - ' + str(user.get('order_food',
                                               config['DEFAULT_ORDER']))) if with_orders else '')
                        for user in db])

    total_orders = Counter(p_list.split())['True']

    return (p_list + '\n\n' + config['BOT']['TOTAL_USERS'] + str(len(db)) +
            (('\n' + config['BOT']['TOTAL_ORDERS'] + str(total_orders)) if with_orders else '')) \
        if len(p_list) else config['BOT']['EMPTY']


def clear_orders():
    db.update({'order_food': False})
    logging.info('Cleared orders')


def extract_args(message_text: str):
    return message_text.split()[1:]


get_data_process = multiprocessing.Process(
    target=execute_at, args=(config['ASK_TIME'], get_food_orders, True))
send_data_process = multiprocessing.Process(
    target=execute_at, args=(config['SEND_TIME'], send_food_orders, True))


@bot.message_handler(commands=['start', 'help'])
def start_menu(message: types.Message):
    bot.reply_to(message, config['BOT']['START_MESSAGE'])
    u = message.chat
    user_str = u.first_name + (u.last_name if u.last_name else '')

    logging.info('/start or /help from %s:%s', u.id, user_str)

    if not is_user(u.id) and not is_admin(u.id):
        add_user_keyboard = types.InlineKeyboardMarkup(row_width=1)
        add_user_keyboard.add(
            types.InlineKeyboardButton(
                text=config['BOT']['KEYBOARDS']['ADD_TO_DB'],
                callback_data=f'{u.id}:{user_str}'
            ))

        send_to_admins(
            config['BOT']['NEW_USER'] +
            f' {u.id}, {u.username}, {user_str}',
            kwargs={'reply_markup': add_user_keyboard})


@bot.message_handler(commands=['commands'])
def admin_menu(message: types.Message):
    bot.send_message(message.chat.id, config['BOT']['ADMIN_COMMANDS'])

    logging.info('/commands from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.message_handler(commands=['logs'])
def send_logs(message: types.Message):
    u_id = message.chat.id

    if not is_admin(u_id):
        bot.send_message(u_id, config['BOT']['NO_PERMISSION'])
        return

    logging.info('/logs from %s:%s', u_id, message.chat.first_name)

    doc = open(config['LOG_PATH'], 'rb')
    bot.send_document(u_id, doc)

    logging.info('Sent %s file to %s:%s',
                 config['LOG_PATH'], u_id, message.chat.first_name)


@bot.message_handler(commands=['ask_now'])
def request_orders(message: types.Message):
    u_id = message.chat.id

    if not is_admin(u_id):
        bot.send_message(u_id, config['BOT']['NO_PERMISSION'])
        return

    get_food_orders()
    bot.send_message(u_id, config['BOT']['SUCCESS'])

    logging.info('/ask_now from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.message_handler(commands=['orders'])
def send_orders(message: types.Message):
    u_id = message.chat.id

    if not is_admin(u_id):
        bot.send_message(u_id, config['BOT']['NO_PERMISSION'])
        return

    bot.send_message(u_id, config['BOT']['USERS_LIST_TITLE'] +
                     generate_users_str(with_orders=True))

    logging.info('/orders from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.message_handler(commands=['clear_orders'])
def clear(message: types.Message):
    clear_orders()

    bot.send_message(message.chat.id, config['BOT']['SUCCESS'])

    logging.info('/clear_orders from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.message_handler(commands=['users'])
def manage_users(message: types.Message):
    u_id = message.chat.id

    if not is_admin(u_id):
        bot.send_message(u_id, config['BOT']['NO_PERMISSION'])
        return

    bot.send_message(u_id, config['BOT']['USERS_LIST_TITLE'] +
                     generate_users_str(with_ids=True))

    logging.info('/users from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.message_handler(commands=['del_user'])
def delete_user(message: types.Message):
    command_args = extract_args(message.text)
    u_id = message.chat.id

    if not is_admin(u_id):
        bot.send_message(u_id, config['BOT']['NO_PERMISSION'])
        return

    if len(command_args) != 1:
        bot.send_message(u_id, config['BOT']['INVALID_SYNTAX'])
        return

    if is_user(command_args[0]):
        db.remove(tinydb.where('telegram_id') == command_args[0])
        bot.send_message(u_id, config['BOT']['SUCCESS'])

    else:
        bot.send_message(u_id, config['BOT']['NO_USER'])

    logging.info('/del_user from %s:%s', message.chat.id,
                 message.chat.first_name)


@bot.callback_query_handler(func=lambda call: True)
def inline_button(callback):
    data = callback.data

    if '.' in data:
        p_id, order = data.split('.')

        db.update({'order_food': True if order == '1' else False},
                  user_query.telegram_id == p_id)

        new_text = config['BOT']['ASK_MESSAGE'] + \
            (config['BOT']['ORDER_TRUE'] if order == '1'
             else config['BOT']['ORDER_FALSE'])

        bot.edit_message_text(
            new_text,
            callback.message.json['chat']['id'],
            callback.message.json['message_id'])

        logging.info('Received order response; id: %s; order: %r',
                     p_id, bool(order))

    elif ':' in data:
        p_id, p_name = data.split(':')

        if db.search(user_query.name == p_name):
            bot.send_message(callback.from_user.id,
                             config['BOT']['ALREADY_EXISTS'])
            return

        db.insert({'telegram_id': p_id, 'name': p_name})
        bot.send_message(p_id, config['BOT']['ADDED'])
        bot.send_message(callback.from_user.id, config['BOT']['SUCCESS'])

        logging.info('Added user to db; data: %s:%s', p_name, p_id)


@bot.message_handler(func=lambda x: True)
def garbage_handler(message: types.Message):
    bot.send_message(message.chat.id, config['BOT']['GARBAGE_RESPONSE'])

    logging.info('Garbage message from %s:%s', message.chat.id,
                 message.chat.first_name)


if __name__ == '__main__':
    get_data_process.start()
    send_data_process.start()

    bot.polling(none_stop=True)
