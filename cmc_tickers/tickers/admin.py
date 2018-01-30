from django.contrib import admin

from  tickers.models import *

#admin.site.register(tickers.models.Ticker)
#admin.site.register(tickers.models.TickerHistory)

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol',)
