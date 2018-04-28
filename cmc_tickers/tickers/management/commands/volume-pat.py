import sys
from django.core.management.base import BaseCommand
from  tickers.models import *
from  tickers.utils import * # get_time_ago, get_day_trading_of_mcap_percent
import humanize
from datetime import timedelta
from django.utils import timezone
import datetime

class Command(BaseCommand):
    MINIMUM_READINGS_TO_PROCESS_TICKER_AS_INTERESTING_TO_WATCH = 100
    help = 'Find ticker with increasing/decreasing volume patterns.'
    l_tokens_perfect = []
    ONLY_PERFECT_IF_AVG_VOLUME_TO_MCAP_PERCENT_ABOVE_X = 4

    def add_arguments(self, parser):
        #parser.add_argument('-w', '--workers', type=int, default=1, help='number of workers.')
        parser.add_argument('-d', '--days', type=int, default=5, help='Number of days backwards to look back on coin history from now')
        parser.add_argument('-s', '--symbol', type=str, default=None, help='Specific symbol name')
        parser.add_argument('-t', '--alerttp', type=int, default=10, help='Alert when 24 volume / mcap percent above')
        parser.add_argument('-r', '--alertrrp', type=int, default=10, help='Alert rank rise percent')
        parser.add_argument('-mr', '--minreads', type=int, default=self.MINIMUM_READINGS_TO_PROCESS_TICKER_AS_INTERESTING_TO_WATCH, help='minimum readings to even start analyze a coin')
        #parser.add_argument('--workers-timeout', type=int)

    def handle(self, *args, **options):
        symbol = options['symbol']

        self.days_in_history_to_look_back = int(options['days'])
        self.alert_trading_volume_percent_th = int(options['alerttp'])
        self.alert_rank_rise_percent_th = int(options['alertrrp'])
        self.minimum_readings_to_analyze_coin = int(options['minreads'])
        self.i_alert_rise_in_rank_count=0

        print("Started with symbol: %s (max %d days back)" % (symbol, self.days_in_history_to_look_back))

        print("Started with alert_trading_volume_percent_th: %s" % (self.alert_trading_volume_percent_th))
        print("Started with alert_rank_rise_percent_th: %s" % (self.alert_rank_rise_percent_th))
        if symbol:
            symbol = symbol.upper()

        print("Started with %s" % symbol if symbol else "no specific symbol (will go over all of them)")

        dt_limit_time = datetime.datetime.now(tz=timezone.utc)-timedelta(days=self.days_in_history_to_look_back)

        if symbol:
            rs_which_coins = None
            rs = TickerHistory.objects.filter(symbol=symbol).filter(lastUpdated__gte=dt_limit_time).order_by('-lastUpdated')
        else:
            rs_which_coins = Ticker.objects.all().order_by('-rank')

        if rs_which_coins:

            for rec_coin in rs_which_coins:
                rs = TickerHistory.objects.filter(symbol=rec_coin.symbol).filter(lastUpdated__gte=dt_limit_time).order_by('-lastUpdated')
                if len(rs)>self.minimum_readings_to_analyze_coin:
                    self.print_ticker_history_rs_data(rs)
                else:
                    print("== Skipping %s with %s readings in total (min: %s)\r\n" % (rec_coin.symbol, len(rs), self.minimum_readings_to_analyze_coin))
        else:
            self.print_ticker_history_rs_data(rs)

        #
        #
        #
        print("There are %d Perfect tokens - %s" % (len(self.l_tokens_perfect), ",".join(self.l_tokens_perfect) ))

    def print_ticker_history_rs_data(self, rs_TickerHistory):
        rs = rs_TickerHistory
        if rs:
            which_symbol = None
            rank_seen = None
            mcap_seen = None
            value_btc_seen = None
            trading24tomcap = None
            s_prev_displayed_percent_reading_in_period = None
            fl_coin_latest_base_btc_value = None

            sum_24h_trading_volume_to_mcad = 0
            count_24h_trading_volume_to_mcad = 0

            count_available_ticker_readings = len(rs)
            SHOW_X_TICKER_READINGS = 10

            print_reading_modulo = int(count_available_ticker_readings / SHOW_X_TICKER_READINGS)
            print("%s readings (%s per aggregation)" % (count_available_ticker_readings, print_reading_modulo))


            flt_max_24h_trading_volume_to_mcad_seen = None
            #
            print("=======================\r\n")
            for indx_of_available_reading, reading in enumerate(rs):
                s_percent = get_day_trading_of_mcap_percent_for_obj(obj=reading)
                if s_percent != None:
                    fl_percent_24h_trading_volume_to_mcad = float(s_percent.replace('%', ''))
                else:
                    fl_percent_24h_trading_volume_to_mcad = None

                current_available_reading_percent_in_available_period = int((indx_of_available_reading / count_available_ticker_readings) * 100)
                if current_available_reading_percent_in_available_period % SHOW_X_TICKER_READINGS == 0 or indx_of_available_reading+1 == len(rs):
                    if indx_of_available_reading+1 == len(rs):
                        s_displayed_percent_reading_in_period = 100
                    else:
                        s_displayed_percent_reading_in_period = current_available_reading_percent_in_available_period

                # Print ticker if last ticker read (oldest one) or if we reached far enough from previous printed ticker
                if (indx_of_available_reading % print_reading_modulo == 0 and s_displayed_percent_reading_in_period != s_prev_displayed_percent_reading_in_period) or indx_of_available_reading+1 == len(rs):
                    if fl_coin_latest_base_btc_value != None:
                        percent_change_from_latest_btc_price = int(((fl_coin_latest_base_btc_value-reading.priceBtc) / reading.priceBtc)*100)
                        s_change_from_base_btc_value = " : %d%% %s within %s days" % (abs(percent_change_from_latest_btc_price), "gain" if percent_change_from_latest_btc_price >= 0 else "loss", (coin_latest_base_last_updated-reading.lastUpdated).days)
                    else:
                        s_change_from_base_btc_value = ""

                    print("%s%% - %s symbol ticker was read %s, rank #%s, value %s BTC (%s%% daily change) with %s trading percent (MCAP: %s)%s" % \
                          (s_displayed_percent_reading_in_period, reading.symbol, get_time_ago(reading.lastUpdated), reading.rank, reading.priceBtc, reading.percentChange24h, s_percent, format_using_humanize(reading.markedCapUsd, humanize.intword),
                          s_change_from_base_btc_value) \
                          )
                    if s_prev_displayed_percent_reading_in_period == None: # save base
                        fl_coin_latest_base_btc_value = reading.priceBtc
                        coin_latest_base_last_updated = reading.lastUpdated

                    s_prev_displayed_percent_reading_in_period = s_displayed_percent_reading_in_period

                if fl_percent_24h_trading_volume_to_mcad != None:
                    sum_24h_trading_volume_to_mcad += fl_percent_24h_trading_volume_to_mcad
                    count_24h_trading_volume_to_mcad += 1

                    if flt_max_24h_trading_volume_to_mcad_seen == None or flt_max_24h_trading_volume_to_mcad_seen < fl_percent_24h_trading_volume_to_mcad:
                        flt_max_24h_trading_volume_to_mcad_seen = fl_percent_24h_trading_volume_to_mcad

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
                # value
                if not value_btc_seen or reading.priceBtc > value_btc_seen[1] or reading.priceBtc < value_btc_seen[0]:
                    if not value_btc_seen:
                        value_btc_seen = [reading.priceBtc , reading.priceBtc]
                    else:
                        if reading.priceBtc > value_btc_seen[1]:
                            value_btc_seen[1] = reading.priceBtc

                        if reading.priceBtc < value_btc_seen[0]:
                            value_btc_seen[0] = reading.priceBtc

                # 24h trading / mcap
                if fl_percent_24h_trading_volume_to_mcad != None:
                    if not trading24tomcap or fl_percent_24h_trading_volume_to_mcad > trading24tomcap[1] or fl_percent_24h_trading_volume_to_mcad < trading24tomcap[0]:
                        if not trading24tomcap:
                            trading24tomcap = [fl_percent_24h_trading_volume_to_mcad , fl_percent_24h_trading_volume_to_mcad]
                        else:
                            if fl_percent_24h_trading_volume_to_mcad > trading24tomcap[1]:
                                trading24tomcap[1] = fl_percent_24h_trading_volume_to_mcad

                            if fl_percent_24h_trading_volume_to_mcad < trading24tomcap[0]:
                                trading24tomcap[0] = fl_percent_24h_trading_volume_to_mcad

                # mcap
                if reading.markedCapUsd != None:
                    if not mcap_seen or reading.markedCapUsd > mcap_seen[1] or reading.markedCapUsd < mcap_seen[0]:
                        if not mcap_seen:
                            mcap_seen = [reading.markedCapUsd , reading.markedCapUsd]
                        else:
                            if reading.markedCapUsd > mcap_seen[1]:
                                mcap_seen[1] = reading.markedCapUsd

                            if reading.markedCapUsd < mcap_seen[0]:
                                mcap_seen[0] = reading.markedCapUsd


            if flt_max_24h_trading_volume_to_mcad_seen != None and self.alert_trading_volume_percent_th != None and \
               int(flt_max_24h_trading_volume_to_mcad_seen) > self.alert_trading_volume_percent_th:
                print("-- ALERT %s 24h trading / mcap" % (flt_max_24h_trading_volume_to_mcad_seen))

            rank_most_recent_or_now = rs[0].rank
            rank_oldest_logged = rs[len(rs)-1].rank


            avg_24h_trading_volume_to_mcad = round(sum_24h_trading_volume_to_mcad / count_24h_trading_volume_to_mcad, 1) if count_24h_trading_volume_to_mcad else None

            s_alert_rise_in_rank = ""
            if  rank_oldest_logged > rank_most_recent_or_now:
                percent_rank_rise = int((rank_oldest_logged - rank_most_recent_or_now ) / rank_oldest_logged * 100)
                if  percent_rank_rise > self.alert_rank_rise_percent_th:

                    s_detection_word = "Hey"
                    if avg_24h_trading_volume_to_mcad != None and avg_24h_trading_volume_to_mcad > self.ONLY_PERFECT_IF_AVG_VOLUME_TO_MCAP_PERCENT_ABOVE_X:
                        s_detection_word = "Perfect"
                        self.l_tokens_perfect.append(which_symbol)

                    s_alert_rise_in_rank = "%d) %s, %s rank rises from rank #%s to rank #%s (+%s positions - %s%%)\r\n" % \
                        (self.i_alert_rise_in_rank_count+1, s_detection_word, reading, rank_oldest_logged, rank_most_recent_or_now, rank_oldest_logged - rank_most_recent_or_now, percent_rank_rise)


            if s_alert_rise_in_rank != "":
                self.i_alert_rise_in_rank_count += 1



            print("=======================\r\n"
                    "Summray for %s:\r\n"
                    "%s Rank: #%s - #%s (latest rank: #%s)\r\n"
                    "%s Value: %s - %s BTC (latest value: %s BTC)\r\n"
                    "%s MCAP: %s - %s (latest Market Cap: %s)\r\n"
                    "%s 24h Trading / MCAP: %s%% - %s%% (latest Trading / MCAP: %s, Avg. Trading / MCAP: %s%% from %d readings)\r\n"
                    "%s"%
                    (which_symbol,
                     which_symbol, rank_seen[0], rank_seen[1], rs[0].rank,
                     which_symbol, value_btc_seen[0], value_btc_seen[1], rs[0].priceBtc,
                     which_symbol, format_using_humanize(mcap_seen[0] if mcap_seen != None else None, humanize.intword), format_using_humanize(mcap_seen[1]  if mcap_seen != None else None, humanize.intword),
                     format_using_humanize(rs[0].markedCapUsd, humanize.intword),
                     which_symbol, round(trading24tomcap[0],1) if trading24tomcap != None else None, round(trading24tomcap[1],1) if trading24tomcap != None else None, get_day_trading_of_mcap_percent_for_obj(obj=rs[0]),
                     avg_24h_trading_volume_to_mcad,
                     count_24h_trading_volume_to_mcad,
                     s_alert_rise_in_rank
                     )
                  )





