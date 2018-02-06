## cmc_tickers

# Running

docker-compose build
docker-compose up

# Requires

docker-compose/docker

# Scraper Configuration

To change scraper range, change its [-t] parameter in run_scraper.sh


# Run on Droplet like so newest version
docker-compose stop && git pull && docker-compose build && docker-compose up -d

# Connect to running image
docker ps
docker exec -it cmctickers_scraper_1  bash


docker exec -it 24 bash

# Run the management commands on
cd cmc_tickers/ && python manage.py  volume-pat --alertt 25


# Idea

Every coin with at least 100 readings (3-4 days monitoring) - see

QUN - 389 to 306 within 6 days, show maximum of 10 readings to show progress.

Save every new day any new alert we see "Rise Rank above x%", from x to y