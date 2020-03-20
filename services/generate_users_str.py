def generate_users_str(db, user_query, config, with_orders=False, with_ids=False):
    base = ''

    for user in db:
        base += user['telegram_id'] + ' - ' if with_ids else ''
        base += user['name']
        base += ' - ' + str(user.get('order_food',
                                     config['DEFAULT_ORDER'])) if with_orders else ''
        base += '\n'

    if not len(db):
        return config['BOT']['EMPTY']

    total_orders = db.count(user_query.order_food == True)

    base += '\n' + config['BOT']['TOTAL_USERS'] + str(len(db))
    base += '\n' + config['BOT']['TOTAL_ORDERS'] + \
        str(total_orders) if with_orders else ''

    return base
