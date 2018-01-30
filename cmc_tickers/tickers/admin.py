from django.contrib import admin
import timeago
from  tickers.models import *
import datetime
#admin.site.register(tickers.models.Ticker)
#admin.site.register(tickers.models.TickerHistory)

def format_time_ago_lastUpdated(obj):
    return timeago.format(obj.lastUpdated.replace(tzinfo=None) , datetime.datetime.now().replace(tzinfo=None))
format_time_ago_lastUpdated.short_description = 'last Updated'
format_time_ago_lastUpdated.allow_tags = True
format_time_ago_lastUpdated.admin_order_field = 'lastUpdated'

def format_time_ago_dateAdded(obj):
    return timeago.format(obj.dateAdded.replace(tzinfo=None) , datetime.datetime.now().replace(tzinfo=None))
format_time_ago_dateAdded.short_description = 'date Added'
format_time_ago_dateAdded.allow_tags = True
format_time_ago_dateAdded.admin_order_field = 'dateAdded'


@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'priceBtc', 'priceUsd', format_time_ago_lastUpdated, format_time_ago_dateAdded)
    ordering = ('rank', )
    list_filter = ('symbol',)
    search_fields = ['name', 'symbol' ]
