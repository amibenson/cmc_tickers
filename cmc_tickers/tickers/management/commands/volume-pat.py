import sys
from django.core.management.base import BaseCommand
from  tickers.models import *
from  tickers.utils import * # get_time_ago, get_day_trading_of_mcap_percent
import humanize

class Command(BaseCommand):
    help = 'Find ticker with increasing/decreasing volume patterns.'

    def add_arguments(self, parser):
        #parser.add_argument('-w', '--workers', type=int, default=1, help='number of workers.')
        parser.add_argument('-s', '--symbol', type=str, default=None, help='Specific symbol name')
        parser.add_argument('-t', '--alertt', type=int, default=10, help='Alert when 24 volume / mcap above 10')
        #parser.add_argument('--workers-timeout', type=int)

    def handle(self, *args, **options):
        symbol = options['symbol']
        alert_trading_volume_percent_th = float(options['alertt'])

        print("Started with symbol: %s" % (symbol))
        print("Started with alert_trading_volume_percent_th: %s" % (alert_trading_volume_percent_th))
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
        which_symbol = None
        rank_seen = None
        value_seen = None


        flt_max_24h_trading_volume_to_mcad_seen = None
        print("=======================\r\n")
        for reading in rs:
            s_percent = get_day_trading_of_mcap_percent_for_obj(obj=reading)
            print("%s symbol ticker was read %s, rank #%s, value %s BTC (%s%% daily change) with %s trading percent (MCAP: %s)" % \
                  (reading.symbol, get_time_ago(reading.lastUpdated), reading.rank, reading.priceBtc, reading.percentChange24h, s_percent, format_using_humanize(reading.markedCapUsd, humanize.intword)) \
                  )
            if flt_max_24h_trading_volume_to_mcad_seen == None or flt_max_24h_trading_volume_to_mcad_seen < float(s_percent.replace('%', '')):
                flt_max_24h_trading_volume_to_mcad_seen = float(s_percent.replace('%', ''))

            if not which_symbol:
                which_symbol = reading.symbol

            if not rank_seen or reading.rank > rank_seen[1] or reading.rank < rank_seen[0]:
                if not rank_seen:
                    rank_seen = (reading.rank , reading.rank )
                else:
                    if reading.rank > rank_seen[1]:
                        rank_seen[1] = reading.rank

                    if reading.rank < rank_seen[0]:
                        rank_seen[0] = reading.rank


        if flt_max_24h_trading_volume_to_mcad_seen != None and alert_trading_volume_percent_th != None and \
           flt_max_24h_trading_volume_to_mcad_seen > float(alert_trading_volume_percent_th):
            print("-- ALERT %s 24h trading / mcap" % (flt_max_24h_trading_volume_to_mcad_seen))

        print("=======================\r\nSummray for %s:\r\nRank: %s to %s\r\n" % (which_symbol, rank_seen[0], rank_seen[1]))





