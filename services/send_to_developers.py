import logging


def send_to_developers(bot, config, message_text, args=(), kwargs={}):
    for dev in config['DEVELOPERS']:
        try:
            bot.send_message(dev, message_text, *args, **kwargs)

            logging.info('Sent message to developer (%s); message: %s',
                         dev, message_text)
        except:
            logging.info('Unable to send message to developer; id: %s', dev)
