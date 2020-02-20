def is_user(u_id, db):
    return str(u_id) in [p['telegram_id'] for p in db]
