import logging
import schedule
import threading
import time
import WeeklyScraper


def startLogging():
    logging.basicConfig(filename='/usr/logs/logs.log', format='%(levelname)s: %(filename)s:%(lineno)d - %(message)s:',encoding='utf-8', level=logging.DEBUG)

    # Remove logging debug logs
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.debug("Logging has started")

def scrapeWeekInThread():
    jobThread = threading.Thread(target=WeeklyScraper.scrapeStats)
    jobThread.start()


schedule.every().thursday.at("01:30").do(scrapeWeekInThread)
def main():
    startLogging()
    # When the container is officially running it will scrape every Tuesday at 1:30 AM
    # (hopefully they will have all of the stats out by then)
    while True:
        schedule.run_pending()
        time.sleep(60)
