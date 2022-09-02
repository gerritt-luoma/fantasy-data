import schedule
from utils import RequestUtils
from utils import ScrapingUtils

def main():
    # print('hello world')
    # pageContent = RequestUtils.getContent('https://www.pro-football-reference.com/years/2021/week_1.htm')
    # gameLinks = ScrapingUtils.getWeeklyGames(pageContent)
    # print(gameLinks)
    # while True:
    #     Eventually this will fire one per week very early Tuesday mornings to scrape the weekly data
    #     pass
    pageContent = RequestUtils.getContent('https://www.pro-football-reference.com/boxscores/202109090tam.htm')
    statTables = ScrapingUtils.getStatTables(pageContent)
    pbp = ScrapingUtils.getTableByName('all_scoring', statTables)
    print(pbp)