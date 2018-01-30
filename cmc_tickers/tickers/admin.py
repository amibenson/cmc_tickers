from django.contrib import admin
import timeago
from  tickers.models import *
import datetime
#admin.site.register(tickers.models.Ticker)
#admin.site.register(tickers.models.TickerHistory)

def format_time_ago(obj):
    return timeago.format(obj.lastUpdated , datetime.datetime.now())

format_time_ago.short_description = 'last Updated'
format_time_ago.allow_tags = True
format_time_ago.admin_order_field = 'lastUpdated'

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', format_time_ago)
