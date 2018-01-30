#!/bin/sh

# wait 1 minute for server to start
sleep 60

cd webscraper
python cmc_ticker.py --s http://web:8000 --t 200