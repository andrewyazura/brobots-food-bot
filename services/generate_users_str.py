from collections import Counter


def generate_users_str(db, config, with_orders=False, with_ids=False):
    p_list = '\n'.join([((user['telegram_id'] + ' - ') if with_ids else '')
                        + user['name'] +
                        ((' - ' + str(user.get('order_food',
                                               config['DEFAULT_ORDER']))) if with_orders else '')
                        for user in db])

    total_orders = Counter(p_list.split())['True']

    return (p_list + '\n\n' + config['BOT']['TOTAL_USERS'] + str(len(db)) +
            (('\n' + config['BOT']['TOTAL_ORDERS'] + str(total_orders)) if with_orders else '')) \
        if len(p_list) else config['BOT']['EMPTY']
