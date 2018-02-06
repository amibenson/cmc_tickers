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