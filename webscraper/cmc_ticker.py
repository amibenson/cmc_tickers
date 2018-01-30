import urllib.request
import json
import requests
import datetime
import argparse

from apscheduler.schedulers.blocking import BlockingScheduler

parser = argparse.ArgumentParser(description='Scraper to read top tickers from CoinMarket.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--t', '--top_tickers', type=int, default=100,
                    help='Number of top tickers to be analyzed.')
parser.add_argument('--s', '--server', type=str, default='http://localhost:8000',
                    help='Server url to store read tickers.')

args = parser.parse_args()

number_of_top_tickers_to_be_analyzed = args.t
coin_market_url = 'https://api.coinmarketcap.com/v1/ticker/?limit=' + \
    str(number_of_top_tickers_to_be_analyzed)
server_url = args.s

def parseTicker(data):
    ticker = {}

    ticker['tickerId'] = data['id']
    ticker['name'] = data['name']
    ticker['symbol'] = data['symbol']
    ticker['rank'] = data['rank']
    ticker['priceUsd'] = data['price_usd']
    ticker['priceBtc'] = data['price_btc']
    ticker['dayVolumeUsd'] = data['24h_volume_usd']
    ticker['markedCapUsd'] = data['market_cap_usd']
    ticker['availableSupply'] = data['available_supply']
    ticker['totalSupply'] = data['total_supply']
    ticker['maxSupply'] = data['max_supply']
    ticker['percentChange1h'] = data['percent_change_1h']
    ticker['percentChange24h'] = data['percent_change_24h']
    ticker['percentChange7d'] = data['percent_change_7d']
    ticker['lastUpdated'] = datetime.datetime.fromtimestamp(
        int(data['last_updated']))

    datenow = datetime.datetime.now()
    ticker['lastAnalyzed'] = datenow
    ticker['dateAdded'] = datenow

    return ticker


def readCoinMarket(market_url):
    with urllib.request.urlopen(market_url) as url:
        data = json.loads(url.read().decode())
        return data


def saveData(data):
    r = requests.post(server_url + '/tickers/', data=data)
    print(r.status_code, r.reason)
    print(r.content)


def updateData(data, data_id):
    r = requests.put(server_url + '/tickers/' + str(data_id) + '/', data=data)
    print(server_url + '/tickers/' + str(data_id) + '/')
    print(r.status_code, r.reason)
    print(r.content)


def getExistingData(data):
    with urllib.request.urlopen(server_url + '/tickersWithId/' + data['tickerId']) as url:
        data = json.loads(url.read().decode())
        return data


def runTicker(t):
    ticker = parseTicker(t)
    existingTickers = getExistingData(ticker)

    if len(existingTickers) == 0:
        saveData(ticker)
    else:
        ticker['dateAdded'] = existingTickers[0]['dateAdded']
        updateData(ticker, existingTickers[0]['id'])


def runscraper():
    coinMarketData = readCoinMarket(coin_market_url)

    for t in coinMarketData:
        runTicker(t)

print("Starting webscraper scheduler...")
print("Server: " + server_url)
print("Top tickers: " + str(number_of_top_tickers_to_be_analyzed))
scheduler = BlockingScheduler()
job = scheduler.add_job(runscraper, 'interval', minutes=10)
print("Running schedule...")
runscraper()
scheduler.start()