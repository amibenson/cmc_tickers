import sys
from django.core.management.base import BaseCommand
from  tickers.models import *
from  tickers.utils import * # get_time_ago, get_day_trading_of_mcap_percent



class Command(BaseCommand):
    help = 'Find ticker with increasing/decreasing volume patterns.'

    def add_arguments(self, parser):
        #parser.add_argument('-w', '--workers', type=int, default=1, help='number of workers.')
        parser.add_argument('-s', '--symbol', type=str, default=None, help='Specific symbol name')
        parser.add_argument('-t', '--alertt', type=int, default=10, help='Alert when 24 volume / mcap above 10')
        #parser.add_argument('--workers-timeout', type=int)

    def handle(self, *args, **options):
        symbol = options['symbol']
        alert_trading_volume_percent_th = options['alertt']

        if symbol:
            symbol = symbol.upper()

        print("Started with %s" % symbol if symbol else "no specific symbol (will go over all of them)")

        if symbol:
            rs_which_coins = None
            rs = TickerHistory.objects.filter(symbol=symbol).order_by('-lastUpdated')
        else:
            rs_which_coins = Ticker.objects.all().order_by('-rank')

        if rs_which_coins:
            for rec_coin in rs_which_coins:
                rs = TickerHistory.objects.filter(symbol=rec_coin.symbol).order_by('-lastUpdated')
                print_ticker_history_rs_data(rs, alert_trading_volume_percent_th)
        else:
            print_ticker_history_rs_data(rs, alert_trading_volume_percent_th)

def print_ticker_history_rs_data(rs_TickerHistory, alert_trading_volume_percent_th = None):
    rs = rs_TickerHistory
    if rs:
        print("=======================\r\n")
        for reading in rs:
            s_percent = get_day_trading_of_mcap_percent_for_obj(obj=reading)
            print("%s symbol ticker was read %s, value %s BTC (%s%% daily change) with %s trading percent" % \
                  (reading.symbol, get_time_ago(reading.lastUpdated), reading.priceBtc, reading.percentChange24h, s_percent) \
                  )

            if alert_trading_volume_percent_th and alert_trading_volume_percent_th > float(s_percent.replace('%', '')):
                print("-- ALERT %s 24h trading / mcap" % (s_percent))

        print("=======================\r\n")





