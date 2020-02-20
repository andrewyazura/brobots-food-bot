import logging


def send_to_admins(bot, config, message_text, args=(), kwargs={}):
    for admin in config['ADMINS']:
        bot.send_message(admin, message_text, *args, **kwargs)

        logging.info('Sent message to admin (%s); message: %s',
                     admin, message_text)
