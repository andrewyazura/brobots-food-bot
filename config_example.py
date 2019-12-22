from datetime import time

config = {
    'DB_PATH': './db/parents.json',
    'ASK_TIME': time(0, 0, 0),
    'SEND_TIME': time(1, 42, 6),
    'BOT': {
        'TOKEN': 'your_token',
        'START_MESSAGE': 'Hello world',
        'ASK_MESSAGE': 'How are you?',
        'ACCEPTED': 'Great!'
    },
    'ADMIN_ID': 'admin_id'
}
