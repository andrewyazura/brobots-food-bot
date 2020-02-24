import logging
from services.send_to_admins import send_to_admins
from services.generate_users_str import generate_users_str


def send_food_orders(bot, db, config):
    send_to_admins(bot, config, config['BOT']['USERS_LIST_TITLE'] +
                   generate_users_str(db, config, with_orders=True))

    logging.info('Sent list of orders to admins')
