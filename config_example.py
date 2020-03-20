from datetime import time

config = {
    'DB_PATH': './db/users.json',
    'LOG_PATH': './bot.log',
    'LOG_FORMAT': '%(asctime)s %(levelname)s: %(message)s',

    'ASK_TIME': time(0, 0, 0),
    'SEND_TIME': time(1, 42, 6),

    'DEFAULT_ORDER': False,

    'BOT': {
        'TOKEN': 'your_token',
        'START_MESSAGE': 'Hello world',
        'ASK_MESSAGE': 'Do you want to order?',

        'ORDER_TRUE': 'Orderd!',
        'ORDER_FALSE': 'Not ordered',

        'ADDED': 'Admin added you!',

        'SUCCESS': 'Everything is fine!',
        'NO_PERMISSION': 'You\'re not an admin',

        'INVALID_SYNTAX': 'Error',

        'USERS_LIST_TITLE': 'Users\n',
        'NEW_USER': 'New:',
        'TOTAL_USERS': 'In total: ',
        'TOTAL_ORDERS': 'Orders in total: ',
        'EMPTY': 'Empty...',

        'ALREADY_EXISTS': 'User is already in DB',
        'NO_USER': 'No such user',

        'TROUBLESHOOTING': 'Developer will be notified!',
        'NOT_REGISTERED': 'You\'re not registered! Use /start first and wait until admins submit you',
        'GARBAGE_RESPONSE': 'Stop sending this!',

        'KEYBOARDS': {
            'YES': 'Yep!',
            'NO': 'No...',
            'ADD_TO_DB': 'Add'
        },
        'HELP_MESSAGE': '''Commands:

/ask_me - change your mind

/report <message> - report bug in bot
        ''',
        'ADMIN_COMMANDS': r'''Commands:

/users - all users

/del\_user <id> - remove user by id

/orders - all orders

/clear\_orders - clear orders

/ask\_now _<clear>_ - request orders now
_clear_:
    1 - clear orders before request
    0 - don't clear

/logs - view logs file
        '''
    },
    'ADMINS': ['admin_id', 'another_one'],
    'DEVELOPERS': ['dev_id']
}

if __name__ == '__main__':
    from pprint import pprint

    pprint(config)
