import logging


def clear_orders(db):
    db.update({'order_food': False})
    logging.info('Cleared orders')
