from utils import ScrapingUtils
from utils import RequestUtils
from utils import DBUtils
import time
from datetime import date
import json

baseURL = 'https://www.pro-football-reference.com/'

advancedTableNames = ['all_passing_advanced', 'all_rushing_advanced', 'all_receiving_advanced']

def scrapeGame(gameLink):
    gamePage = RequestUtils.getContent(f'{baseURL}{gameLink}')
    #homeTeam, awayTeam = 
    homeTeam, awayTeam = ScrapingUtils.getTeamNames(gamePage)
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

    gameDict = {
        'home': homeTeam,
        'away': awayTeam,
        'stats': offenseList
    }
    return gameDict

def determineWeek():
    startDate = date(2022, 9, 6)
    todaysDate = date.today()
    daysDifference = todaysDate - startDate
    numWeeks = daysDifference // 7
    return numWeeks

def scrapeStats():
    # will use this once the container is actually running
    # week = determineWeek()
    # weeklyURL = f'{baseURL}years/2022/week_{week}.htm'
    # weekPage = RequestUtils.getContent(weeklyURL)
    week = 1
    weekPage = RequestUtils.getContent('https://www.pro-football-reference.com/years/2021/week_1.htm')
    gameLinks = ScrapingUtils.getWeeklyGameLinks(weekPage)

    weekList = []

    for i, game in enumerate(gameLinks):
        print(f'Scraping game #{i}')
        scrapedGame = scrapeGame(game)
        print(json.dumps(scrapedGame, indent=2, sort_keys=True))

        weekList.append(scrapedGame)

        # Sleep for 3 second so I don't get banned lmao
        time.sleep(3)
    DBUtils.writeToDatabase(week, weekList)
