from telebot import types


def generate_order_keyboard(user_id, config):
    keyboard_options = types.InlineKeyboardMarkup(row_width=2)
    keyboard_options.add(types.InlineKeyboardButton(
        text=config['BOT']['KEYBOARDS']['YES'], callback_data=f'{user_id}.1'))
    keyboard_options.add(types.InlineKeyboardButton(
        text=config['BOT']['KEYBOARDS']['NO'], callback_data=f'{user_id}.0'))

    return keyboard_options
