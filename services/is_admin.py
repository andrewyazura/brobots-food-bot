def is_admin(u_id, config):
    return str(u_id) in config['ADMINS']
