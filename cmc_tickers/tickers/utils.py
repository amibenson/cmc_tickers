import timeago
import datetime


def get_time_ago(date_older, date_newer = datetime.datetime.now()):
    return timeago.format(date_older.replace(tzinfo=None), date_newer.replace(tzinfo=None))

def get_day_trading_of_mcap_percent_for_obj(obj):
    return get_day_trading_of_mcap_percent(obj.dayVolumeUsd, obj.markedCapUsd)

def get_day_trading_of_mcap_percent(dayVolumeUsd, markedCapUsd):
    return '{0:.1f}%'.format(dayVolumeUsd / markedCapUsd * 100)


