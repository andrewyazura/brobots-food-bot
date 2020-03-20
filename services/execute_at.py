from datetime import datetime, timedelta
import logging
import time


def is_business_day(date):
    return date.weekday() < 5


def execute_at(wake_time: datetime.time, callback, only_business: bool,
               args=(), kwargs={}, interval=timedelta(days=1)):
    wake_time = datetime.combine(datetime.now(), wake_time)

    while True:
        time.sleep(1)
        now = datetime.now()

        if only_business and not is_business_day(now):
            continue

        if now >= wake_time:
            callback(*args, **kwargs)
            wake_time += interval

            logging.info('Executing %s at %r', callback.__name__, wake_time)
