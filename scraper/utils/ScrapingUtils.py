from bs4 import BeautifulSoup, Comment
import hashlib
import logging
"""
    A collection of utility functions used for scraping the weekly game statistics from PFR
"""

# getSoup takes raw html as an input attempts to parse it with BeautifulSoup, and returns the result
# If the result is a failure, it is none
def getSoup(content):
    contentSoup = None
    try:
        contentSoup = BeautifulSoup(content, 'html.parser')
    except:
        logging.error("There was an error converting content to soup")
    return contentSoup

# getWeeklyGameLinks takes the raw html of the weekly games page from PFR
# and finds all of the links to the individual game box scores.  Returns a list of links if successful, else none
def getWeeklyGameLinks(gamesPage):
    gamesPageSoup = getSoup(gamesPage)
    gamesLinks = None
    if gamesPageSoup:
        gamesDiv = gamesPageSoup.find('div', { 'class' : 'game_summaries' })
        gamesList = gamesDiv.find_all('table', { 'class': 'teams' })
        gamesLinks = []
        for game in gamesList:
            teamsData = game.find('td', { 'class': 'gamelink'})
            link = teamsData.find('a')
            if link.has_attr('href'):
                gamesLinks.append(link['href'])
            else:
                logging.warning(f'Could not extract link')
    return gamesLinks

# getTeamNames takes the singlular game page html and finds the team names from the title of the page
def getTeamNames(gamePage):
    gamePageSoup = getSoup(gamePage)
    title = gamePageSoup.title.string
    teams = title.split(' - ')[0]
    away, home = teams.split(' at ')
    return home, away

# getStatTableDivs takes in the raw game page html and returns a list of the divs containing all stat tables
def getStatTableDivs(gamePage):
    gamePageSoup = getSoup(gamePage)
    statTableDivs = None
    if gamePageSoup:
        statTableDivs = gamePageSoup.find_all('div', { 'class': 'table_wrapper'})
    return statTableDivs

# getTableByName searches the inputted list for a table containing an id matching the inputted id
def getTableByName(name, tables):
    return next((table for table in tables if table['id'] == name), None)

# getTableHeadAndBody takes in the table div of a stat and extracts the thead and tbody of the table
def getTableHeadAndBody(tableDiv):
    fullTable = tableDiv.find('table')

    tableHead = fullTable.find('thead')
    tableBody = fullTable.find('tbody')
    return tableHead, tableBody

# getBasicOverHeaderCounts is used for the basic stats to keep track of what stats fall under what category.  Returns 5 integers
def getBasicOverHeaderCounts(head):
    overheader = head.find_all('tr')[0].find_all('th')
    colCounts = [int(col['colspan']) for col in overheader]
    numInfo = colCounts[0]
    numPassing = sum(colCounts[:2])
    numRushing = sum(colCounts[:3])
    numReceiving = sum(colCounts[:4])
    numFumbles = sum(colCounts)
    return numInfo, numPassing, numRushing, numReceiving, numFumbles

# getStatKeys iterates through the head of the table and retrieves the name of each statistic storing them in a list
def getStatKeys(head):
    stats = head.find_all('tr')[-1].find_all('th')
    statKeys = [stat.text.lower() for stat in stats]
    return statKeys

# getPlayerId grabs the link from the name cell and hashes it using md5.  This is to ensure we have unique player ids
# in the event of repeated names like "Mike Smith"
def getPlayerId(cell):
    atag = cell.find('a')
    link = atag['href']
    return hashlib.md5(link.encode()).hexdigest()

# findPlayerById searches the inputted list of players to find a player with a matching id
def findPlayerById(id, players):
    return next((player for player in players if player['player_id'] == id), None)

# convertStatIfNecessary takes in the text of a stat cell.  If it is empty, change to a '0'.
# Strip all % signs and convert to float/integer if necessary
def convertStatIfNecessary(stat):
    if stat == '':
        stat = '0'
    stat = stat.replace('%', '')
    if stat.replace('.','',1).isnumeric():
        stat = float(stat)
        if stat.is_integer():
            stat = int(stat)
    return stat

# scrapeBasicOffense is used to scrape the table containing all basic stats of
# passing, receiving, rushing, and fumbles as well as pulling the names of the players
# returns a list of dictionaries containing the scraped info
def scrapeBasicOffense(head, body, homeTeam, awayTeam):
    # Absolutely YUUUUUGE function.  Could potentially break it down

    # This is a fat declaration
    numInfo, numPassing, numRushing, numReceiving, numFumbles = getBasicOverHeaderCounts(head)

    statKeys = getStatKeys(head)

    # Find all rows of the basic stat table and initialize the output list
    bodyRows = body.find_all('tr')
    offenseList = []

    # Iterate through each row to gather player stats
    for row in bodyRows:
        # There are some rows that contain unnecessary data.  These rows contain a class while the rest do not.
        if not row.has_attr('class'):
            # Find all th and trs
            cells = row.find_all(recursive=False)
            player = {
                'home': homeTeam,
                'away': awayTeam,
                'info': {},
                'passing': {},
                'rushing': {},
                'receiving': {},
                'fumbles': {}
            }

            # To properly sort all stats to the correct dict I need to do some counting magic
            count = 0
            for stat, cell in zip(statKeys, cells):
                value = convertStatIfNecessary(cell.text)
                if count == 0:
                    player['player_id'] = getPlayerId(cell)
                if count < numInfo:
                    player['info'][stat] = value
                elif count < numPassing:
                    player['passing'][stat] = value
                elif count < numRushing:
                    player['rushing'][stat] = value
                elif count < numReceiving:
                    player['receiving'][stat] = value
                elif count < numFumbles:
                    player['fumbles'][stat] = value
                else:
                    logging.warning(f'Should never get here.\nstat: {stat}, value: {value}')
                count += 1
            
            # To save up on storage space I should remove all sub dicts that only contain 0
            # Probably a pretty choppy way of doing this.  May want to refactor in the future
            for key in player.copy():
                if key != 'player_id' and key != 'info' and key != 'home' and key != 'away':
                    allZeros = all(value == 0 for value in player[key].values())
                    if allZeros:
                        del player[key]

            # Add player to the output
            offenseList.append(player)
    return offenseList

# getAdvancedTableFromComment is used to pull the advanced tables from within comment tags in the html
# PFR thinks they're slick by just hiding the data within the comments if you aren't a paid user lmao
def getAdvancedTableFromComment(tableDiv):
    table = tableDiv.find(text=lambda text:isinstance(text, Comment))
    return BeautifulSoup(table, 'html.parser')

# scrapeAdvancedTable is used to scrape the advanced statistics tables and add the advanced data to the matching players
def scrapeAdvancedTable(head, body, statName, offenseList):
    # Get the keys for all stats in the advanced table
    statKeys = getStatKeys(head)

    # Find all rows and iterate through
    rows = body.findAll('tr')
    for row in rows:
        # Same as basic table.  There are unnecessary rows in the body that need to be removed.
        if not row.has_attr('class'):
            count = 0
            statDict = {}
            playerID = None
            stats = row.findAll(recursive=False)

            # Iterate through each stat in the row
            for key, stat in zip(statKeys, stats):
                # If count == 0 we know the player link is in this cell.  Use this cell to get the player id
                if count == 0:
                    playerID = getPlayerId(stat)

                # The first two cells in each row is the name and team abbreviation.  Skip these.
                if count < 2:
                    count += 1
                    continue

                value = convertStatIfNecessary(stat.text)
                statDict[key] = value
            # Get pointer to player dictionary in offense list and add new stat dict to list
            player = findPlayerById(playerID, offenseList)
            player[statName] = statDict
