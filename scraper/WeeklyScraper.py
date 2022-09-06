from utils import ScrapingUtils
from utils import RequestUtils
from utils import DBUtils
import time
from datetime import date
import json
import logging

baseURL = 'https://www.pro-football-reference.com/'

advancedTableNames = ['all_passing_advanced', 'all_rushing_advanced', 'all_receiving_advanced']

def scrapeGame(gameLink):
    gamePage = None
    homeTeam, awayTeam = None, None
    statTableDivs = None
    basicScoringTable = None
    head, body = None
    offenseList = None

    # Try to get the gamePage
    try:
        gamePage = RequestUtils.getContent(f'{baseURL}{gameLink}')
    except:
        logging.error('Failed to get game page')
        logging.exception('')
        # Failed to get game page.  Exit out of function.
        return None

    # Attempt to get team names
    try:
        homeTeam, awayTeam = ScrapingUtils.getTeamNames(gamePage)
        logging.info(f'Now scraping {awayTeam} at {homeTeam}')
    except:
        logging.error('Failed to get team names')
        logging.exception('')
        # Failed to get team names. Exit out of function.
        return None

    # Attempt to get the stat table divs
    try:
        statTableDivs = ScrapingUtils.getStatTableDivs(gamePage)
    except:
        logging.error('Failed to get stat table divs')
        logging.exception('')
        # Failed to get the stat divs.  Exit from function
        return None

    # Scrape the basic table to the offense list
    try:
        basicScoringTable = ScrapingUtils.getTableByName('all_player_offense', statTableDivs)
        head, body = ScrapingUtils.getTableHeadAndBody(basicScoringTable)
        offenseList = ScrapingUtils.scrapeBasicOffense(head, body)
    except:
        logging.error('Failed to scrape the basic scoring table')
        logging.exception('')
        # Failed to scrape the basic scoring table.  Exit from function

    for tableName in advancedTableNames:
        try:
            advancedStatTableDiv = ScrapingUtils.getTableByName(tableName, statTableDivs)
            advancedStatTable = ScrapingUtils.getAdvancedTableFromComment(advancedStatTableDiv)
            head, body = ScrapingUtils.getTableHeadAndBody(advancedStatTable)

            statName = tableName.replace('all_', '')
            ScrapingUtils.scrapeAdvancedTable(head, body, statName, offenseList)
        except:
            logging.error(f'Failed to scrape the {statName} table')
            logging.exception('')
            return None

    gameDict = {
        'home': homeTeam,
        'away': awayTeam,
        'stats': offenseList
    }
    return gameDict

def determineWeek():
    numWeeks = None
    try:
        startDate = date(2022, 9, 6)
        todaysDate = date.today()
        daysDifference = todaysDate - startDate
        numWeeks = daysDifference // 7
    except:
        logging.error('Failed to calculate number of weeks into season')
        logging.exception('')
    return numWeeks

def scrapeStats():
    # will use this once the container is actually running
    # week = determineWeek()
    # weeklyURL = f'{baseURL}years/2022/week_{week}.htm'
    # weekPage = RequestUtils.getContent(weeklyURL)
    logging.error('This is an error in a different file')
    return
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
    #DBUtils.writeToDatabase(week, weekList)
