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
            MINIMUM_READINGS_TO_PROCESS_TICKER_AS_INTERESTING_TO_WATCH = 100
            for rec_coin in rs_which_coins:
                rs = TickerHistory.objects.filter(symbol=rec_coin.symbol).order_by('-lastUpdated')
                if len(rs)>MINIMUM_READINGS_TO_PROCESS_TICKER_AS_INTERESTING_TO_WATCH:
                    print_ticker_history_rs_data(rs, alert_trading_volume_percent_th)
                else:
                    print("== Skipping %s with %s readings in total\r\n" % (rec_coin.symbol, en(rs)))
        else:
            print_ticker_history_rs_data(rs, alert_trading_volume_percent_th)

def print_ticker_history_rs_data(rs_TickerHistory, alert_trading_volume_percent_th = None):
    rs = rs_TickerHistory
    if rs:
        which_symbol = None
        rank_seen = None
        mcap_seen = None
        value_seen = None
        trading24tomcap = None

        count_available_ticker_readings = len(rs)
        SHOW_X_TICKER_READINGS = 10

        print_reading_modulo = int(count_available_ticker_readings / SHOW_X_TICKER_READINGS)
        print("count_available_ticker_readings: %s" % count_available_ticker_readings)
        print("print_reading_modulo: %s" % print_reading_modulo)

        flt_max_24h_trading_volume_to_mcad_seen = None
        print("=======================\r\n")
        for indx_of_available_reading, reading in enumerate(rs):
            s_percent = get_day_trading_of_mcap_percent_for_obj(obj=reading)

            current_available_reading_percent_in_available_period = int(indx_of_available_reading / 100 * count_available_ticker_readings)
            if current_available_reading_percent_in_available_period % SHOW_X_TICKER_READINGS == 0:
                s_displayed_percent_reading_in_period = current_available_reading_percent_in_available_period

            if indx_of_available_reading % print_reading_modulo == 0:
                print("%s%% - %s symbol ticker was read %s, rank #%s, value %s BTC (%s%% daily change) with %s trading percent (MCAP: %s)" % \
                      (s_displayed_percent_reading_in_period, reading.symbol, get_time_ago(reading.lastUpdated), reading.rank, reading.priceBtc, reading.percentChange24h, s_percent, format_using_humanize(reading.markedCapUsd, humanize.intword)) \
                      )

            if flt_max_24h_trading_volume_to_mcad_seen == None or flt_max_24h_trading_volume_to_mcad_seen < float(s_percent.replace('%', '')):
                flt_max_24h_trading_volume_to_mcad_seen = float(s_percent.replace('%', ''))

            if not which_symbol:
                which_symbol = reading.symbol
            # rank
            if not rank_seen or reading.rank > rank_seen[1] or reading.rank < rank_seen[0]:
                if not rank_seen:
                    rank_seen = [reading.rank , reading.rank]
                else:
                    if reading.rank > rank_seen[1]:
                        rank_seen[1] = reading.rank

                    if reading.rank < rank_seen[0]:
                        rank_seen[0] = reading.rank

            # 24h trading / mcap
            if not trading24tomcap or float(s_percent.replace('%', '')) > trading24tomcap[1] or float(s_percent.replace('%', '')) < trading24tomcap[0]:
                if not trading24tomcap:
                    trading24tomcap = [float(s_percent.replace('%', '')) , float(s_percent.replace('%', ''))]
                else:
                    if float(s_percent.replace('%', '')) > trading24tomcap[1]:
                        trading24tomcap[1] = float(s_percent.replace('%', ''))

                    if float(s_percent.replace('%', '')) < trading24tomcap[0]:
                        trading24tomcap[0] = float(s_percent.replace('%', ''))

            # mcap
            if not mcap_seen or reading.markedCapUsd > mcap_seen[1] or reading.markedCapUsd < mcap_seen[0]:
                if not mcap_seen:
                    mcap_seen = [reading.markedCapUsd , reading.markedCapUsd]
                else:
                    if reading.markedCapUsd > mcap_seen[1]:
                        mcap_seen[1] = reading.markedCapUsd

                    if reading.markedCapUsd < mcap_seen[0]:
                        mcap_seen[0] = reading.markedCapUsd


        if flt_max_24h_trading_volume_to_mcad_seen != None and alert_trading_volume_percent_th != None and \
           flt_max_24h_trading_volume_to_mcad_seen > float(alert_trading_volume_percent_th):
            print("-- ALERT %s 24h trading / mcap" % (flt_max_24h_trading_volume_to_mcad_seen))


        print("=======================\r\n"
                "Summray for %s:\r\n"
                "Rank: %s - %s (%s)\r\n"
                "MCAP: %s - %s (%s)\r\n"
                "24h Trading / MCAP: %s%% - %s%% (%s)\r\n" %
                (which_symbol,
                 rank_seen[0], rank_seen[1], rs[0].rank,
                 format_using_humanize(mcap_seen[0], humanize.intword), format_using_humanize(mcap_seen[1], humanize.intword), format_using_humanize(rs[0].markedCapUsd, humanize.intword),
                 round(trading24tomcap[0],1), round(trading24tomcap[1],1), get_day_trading_of_mcap_percent_for_obj(obj=rs[0]))
              )





