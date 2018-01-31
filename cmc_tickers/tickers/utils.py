import timeago
import datetime


def get_time_ago(date_older, date_newer = datetime.datetime.now()):
    return timeago.format(date_older.replace(tzinfo=None), date_newer.replace(tzinfo=None))