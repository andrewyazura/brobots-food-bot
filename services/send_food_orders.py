import logging
from services.send_to_admins import send_to_admins
from services.generate_users_str import generate_users_str


def send_food_orders(config):
    send_to_admins(config['BOT']['ORDERS_LIST_TITLE'] +
                   generate_users_str(with_orders=True))

    logging.info('Sent list of orders to admins')
