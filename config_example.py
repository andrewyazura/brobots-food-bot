from datetime import time

config = {
    'DB_PATH': './db/users.json',
    'ASK_TIME': time(0, 0, 0),
    'SEND_TIME': time(1, 42, 6),
    'DEFAULT_ORDER': False,
    'BOT': {
        'TOKEN': 'your_token',
        'START_MESSAGE': 'Hello world',
        'ASK_MESSAGE': 'How are you?',
        'ORDER_TRUE': 'Orderd!',
        'ORDER_FALSE': 'Not ordered',
        'ACCEPTED': 'Great!',
        'ADDED': 'Admin added you!',
        'NO_PERMISSION': 'You\'re not an admin',
        'INVALID_SYNTAX': 'Error',
        'SUCCESS': 'Everything is fine!',
        'NO_USER': 'No such user',
        'USERS_LIST_TITLE': 'Users\n',
        'EMPTY': 'Empty...',
        'NEW_USER': 'New:',
        'ALREADY_EXISTS': 'User is already in DB',
        'GARBAGE_RESPONSE': 'Stop sending this!',
        'TOTAL_USERS': 'In total: ',
        'TOTAL_ORDERS': 'Orders in total: ',
        'KEYBOARDS': {
            'YES': 'Yep!',
            'NO': 'No...',
            'ADD_TO_DB': 'Add'
        },
        'ADMIN_COMMANDS': '''Commands:

/users - all users

/del_user <id> - remove user by id

/orders - all orders

/clear_orders - clear orders

/ask_now - send order requests now
        '''
    },
    'ADMINS': ['admin_id', 'another_one']
}

if __name__ == '__main__':
    from pprint import pprint

    pprint(config)
