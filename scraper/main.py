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
    statTableDivs = ScrapingUtils.getStatTableDivs(pageContent)
    allScoring = ScrapingUtils.getTableByName('all_player_offense', statTableDivs)
    head, body = ScrapingUtils.getTableHeadAndBody(allScoring)
    offenseList = ScrapingUtils.scrapeBasicOffense(head, body)
    advancedPassingDiv = ScrapingUtils.getTableByName('all_passing_advanced', statTableDivs)
    advancedPassingTable = ScrapingUtils.getAdvancedTableFromComment(advancedPassingDiv)
    head, body = ScrapingUtils.getTableHeadAndBody(advancedPassingTable)
    offenseList = ScrapingUtils.scrapeAdvancedTable(head, body, 'advanced_passing', offenseList)