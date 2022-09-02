import schedule
import WeeklyScraper
from utils import DBUtils

def main():
    # TODO: Schedule scraper to fire every tuesday morning
    #WeeklyScraper.scrapeStats()
    DBUtils.tryConnecting()