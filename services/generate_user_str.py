def generate_user_str(u):
    return u.first_name + (u.last_name if u.last_name else '')
