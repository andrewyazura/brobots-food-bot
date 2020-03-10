import logging
from services.generate_order_keyboard import generate_order_keyboard


def get_order(bot, config, user):
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
