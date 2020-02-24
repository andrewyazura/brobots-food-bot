import logging


def send_to_admins(bot, config, message_text, args=(), kwargs={}):
    for admin in config['ADMINS']:
        try:
            bot.send_message(admin, message_text, *args, **kwargs)

            logging.info('Sent message to admin (%s); message: %s',
                         admin, message_text)
        except:
            logging.info('Unable to send message to admin; id: %s', admin)
