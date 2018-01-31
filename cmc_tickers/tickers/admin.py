from django.contrib import admin
import timeago
from  tickers.models import *
from  tickers.utils import * # get_time_ago
import datetime
from django.utils.safestring import mark_safe
import humanize
#admin.site.register(tickers.models.Ticker)
#admin.site.register(TickerHistory)

def format_time_ago_lastUpdated(obj):
    return get_time_ago(obj.lastUpdated, datetime.datetime.now())
    #return timeago.format(obj.lastUpdated.replace(tzinfo=None) , datetime.datetime.now().replace(tzinfo=None))
format_time_ago_lastUpdated.short_description = 'last Updated'
format_time_ago_lastUpdated.allow_tags = True
format_time_ago_lastUpdated.admin_order_field = 'lastUpdated'

def format_time_ago_dateAdded(obj):
    return get_time_ago(obj.dateAdded, datetime.datetime.now())

format_time_ago_dateAdded.short_description = 'date Added'
format_time_ago_dateAdded.allow_tags = True
format_time_ago_dateAdded.admin_order_field = 'dateAdded'


def format_day_trading_to_market_cap_percent(obj):
    return  '{0:.1f}%'.format(obj.dayVolumeUsd / obj.markedCapUsd * 100) #"%d" % int((obj.dayVolumeUsd / obj.markedCapUsd) * 100)
format_day_trading_to_market_cap_percent.short_description = 'day trading/mcap'
format_day_trading_to_market_cap_percent.allow_tags = True
format_day_trading_to_market_cap_percent.admin_order_field = 'dayVolumeUsd'


# https://coinmarketcap.com/currencies/iostoken/
def format_name(obj):
    return  mark_safe('%s (%s)<br><small><a href="https://coinmarketcap.com/currencies/%s/" target=_blank>https://coinmarketcap.com/currencies/%s/</a> (<a href="/admin/tickers/tickerhistory/?q=%s" target=_blank>HF</a>)</small><br>' % (obj.name, obj.symbol, obj.name, obj.name, obj.name ))
format_name.short_description = 'name'
format_name.admin_order_field = 'name'

def format_using_humanize(val, format_type):
    if format_type == humanize.intword:
        return humanize.intword(val)


def format_markedCapUsd(obj):
    return format_using_humanize(obj.markedCapUsd, humanize.intword)
format_markedCapUsd.short_description = 'markedCapUsd'
format_markedCapUsd.admin_order_field = 'markedCapUsd'

def format_dayVolumeUsd(obj):
    return format_using_humanize(obj.dayVolumeUsd, humanize.intword)
format_dayVolumeUsd.short_description = 'dayVolumeUsd'
format_dayVolumeUsd.admin_order_field = 'dayVolumeUsd'


#

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('rank', format_name,  'priceBtc', 'priceUsd', format_dayVolumeUsd, 'percentChange24h', format_markedCapUsd,  format_time_ago_lastUpdated, format_time_ago_dateAdded, format_day_trading_to_market_cap_percent)
    ordering = ('rank', )
    list_filter = ('symbol',)
    search_fields = ['name', 'symbol' ]
    list_per_page = 500

@admin.register(TickerHistory)
class TickerHistoryAdmin(admin.ModelAdmin):
    list_display = ('rank', format_name,  'priceBtc', 'priceUsd', format_dayVolumeUsd,  'percentChange24h', format_markedCapUsd, format_time_ago_lastUpdated, format_day_trading_to_market_cap_percent)
    ordering = ('-lastUpdated', )
    list_filter = ('symbol',)
    search_fields = ['name', 'symbol' ]
    list_per_page = 500
