import schedule
import time
import WeeklyScraper
import logging

schedule.every().thursday.at("01:30").do(WeeklyScraper.scrapeStats)

def startLogging():
    logging.basicConfig(filename='/usr/logs/logs.log', format='%(levelname)s: %(filename)s:%(lineno)d - %(message)s:',encoding='utf-8', filemode='w',level=logging.DEBUG)

    # Remove logging debug logs
    logging.getLogger("requests").setLevel(logging.WARNING)

def main():
    startLogging()
    # When the container is officially running it will scrape every Tuesday at 1:30 AM
    # (hopefully they will have all of the stats out by then)
    while True:
        schedule.run_pending()
        time.sleep(60)
