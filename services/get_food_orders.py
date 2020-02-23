import logging
from services.generate_order_keyboard import generate_order_keyboard
from services.clear_orders import clear_orders


def get_food_orders(bot, db, config, clear=False):
    if clear:
        clear_orders(db)

    for user in db:
        kb = generate_order_keyboard(user['telegram_id'], config)

        try:
            bot.send_message(user['telegram_id'],
                             config['BOT']['ASK_MESSAGE'],
                             reply_markup=kb)

            logging.info('Sent request to %s; id: %s',
                         user['name'], user['telegram_id'])

        except:
            logging.info('Unable to send message to %s; id: %s',
                         user['name'], user['telegram_id'])
