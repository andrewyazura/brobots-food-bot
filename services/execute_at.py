import datetime
import logging
import time

from services.is_business_day import is_business_day

from pprint import pprint


def execute_at(wake_time: datetime.time, callback, only_business, args=(), kwargs={}):
    while True:
        now = datetime.datetime.now()

        if only_business and not is_business_day(now):
            continue

        if now.hour == wake_time.hour \
                and now.minute == wake_time.minute \
                and now.second == wake_time.second:
            time.sleep(1)  # without delay it triggers many times a second
            callback(*args, **kwargs)
            logging.info('Executing %s at %r', callback.__name__, wake_time)
