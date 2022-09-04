import schedule
import time
import WeeklyScraper
from utils import DBUtils

schedule.every().tuesday.at("01:30").do(WeeklyScraper.scrapeStats)

def main():
    # When the container is officially running it will scrape every Tuesday at 1:30 AM
    # (hopefully they will have all of the stats out by then)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)


    # Testing ground
    DBUtils.tryConnecting()
