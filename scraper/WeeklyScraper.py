from utils import ScrapingUtils
from utils import RequestUtils
import time

baseURL = 'https://www.pro-football-reference.com/'

advancedTableNames = ['all_passing_advanced', 'all_rushing_advanced', 'all_receiving_advanced']

def scrapeStats():
    # TODO: Determine best way to find how many weeks it's been since the start of the season
    # for now, just testing with week 1 of 2021

    weekPage = RequestUtils.getContent('https://www.pro-football-reference.com/years/2021/week_1.htm')
    gameLinks = ScrapingUtils.getWeeklyGames(weekPage)

    gameList = []
    
    for game in gameLinks:
        gamePage = RequestUtils.getContent(f'{baseURL}{game}')
        statTableDivs = ScrapingUtils.getStatTableDivs(gamePage)
        basicScoringTable = ScrapingUtils.getTableByName('all_player_offense', statTableDivs)
        head, body = ScrapingUtils.getTableHeadAndBody(basicScoringTable)

        offenseList = ScrapingUtils.scrapeBasicOffense(head, body)

        for tableName in advancedTableNames:
            advancedStatTableDiv = ScrapingUtils.getTableByName(tableName, statTableDivs)
            advancedStatTable = ScrapingUtils.getAdvancedTableFromComment(advancedStatTableDiv)
            head, body = ScrapingUtils.getTableHeadAndBody(advancedStatTable)

            statName = tableName.replace('all_', '')
            ScrapingUtils.scrapeAdvancedTable(head, body, statName, offenseList)

        gameList.append(offenseList)

        # Sleep for 5 second so I don't get banned lmao
        time.sleep(5)
