import sys
from django.core.management.base import BaseCommand
from  tickers.models import *
from  tickers.utils import * # get_time_ago, get_day_trading_of_mcap_percent


class Command(BaseCommand):
    help = 'Find ticker with increasing/decreasing volume patterns.'

    def add_arguments(self, parser):
        #parser.add_argument('-w', '--workers', type=int, default=1, help='number of workers.')
        parser.add_argument('-s', '--symbol', type=str, default=None, help='Specific symbol name')
        #parser.add_argument('--workers-timeout', type=int)

    def handle(self, *args, **options):
        symbol    = str(options['symbol'])

        if symbol:
            symbol = symbol.upper()

        print("Started with %s" % symbol if symbol else "no specific symbol (will go over all of them)")

        if symbol:
            rs = TickerHistory.objects.filter(symbol=symbol).order_by('-lastUpdated')

        if rs:
            for reading in rs:
                print("%s symbol at %s - %s BTC with %s% trading percent" % \
                      (reading.symbol, get_time_ago(reading.lastUpdated), reading.priceBtc, get_day_trading_of_mcap_percent_for_obj(obj=reading)) \
                      )




