def extract_args(message_text: str, args=(), kwargs={}):
    return message_text.split(*args, **kwargs)[1:]
