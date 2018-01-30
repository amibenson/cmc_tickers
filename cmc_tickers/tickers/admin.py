from django.contrib import admin
import timeago
from  tickers.models import *
import datetime
#admin.site.register(tickers.models.Ticker)
#admin.site.register(TickerHistory)

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


def format_day_trading_to_market_cap_percent(obj):
    return  '{:.1%}'.format(obj.dayVolumeUsd / obj.markedCapUsd * 100) #"%d" % int((obj.dayVolumeUsd / obj.markedCapUsd) * 100)
format_day_trading_to_market_cap_percent.short_description = 'day trading/mcap'
format_day_trading_to_market_cap_percent.allow_tags = True
format_day_trading_to_market_cap_percent.admin_order_field = 'dayVolumeUsd'



@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name', 'symbol', 'priceBtc', 'priceUsd', 'percentChange24h', format_time_ago_lastUpdated, format_time_ago_dateAdded, format_day_trading_to_market_cap_percent)
    ordering = ('rank', )
    list_filter = ('symbol',)
    search_fields = ['name', 'symbol' ]



"""
    tickerId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    rank = models.IntegerField()
    priceUsd = models.FloatField(null=True, blank=True)
    priceBtc = models.FloatField(null=True, blank=True)
    dayVolumeUsd = models.FloatField(null=True, blank=True)
    markedCapUsd = models.FloatField(null=True, blank=True)
    availableSupply = models.FloatField(null=True, blank=True)
    totalSupply = models.FloatField(null=True, blank=True)
    maxSupply = models.FloatField(null=True, blank=True)
    percentChange1h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange24h = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    percentChange7d = models.DecimalField(
        null=True, blank=True, max_digits=5, decimal_places=2)
    lastUpdated = models.DateTimeField()


"""
@admin.register(TickerHistory)
class TickerHistoryAdmin(admin.ModelAdmin):
    list_display = ('rank', 'name', 'symbol', 'priceBtc', 'priceUsd', 'percentChange24h', format_time_ago_lastUpdated)
    ordering = ('rank', )
    list_filter = ('symbol',)
    search_fields = ['name', 'symbol' ]
