import logging
from services.clear_orders import clear_orders
from services.get_order import get_order


def get_food_orders(bot, db, config, clear=False):
    if clear:
        clear_orders(db)

    for user in db:
        get_order(bot, config, user)
