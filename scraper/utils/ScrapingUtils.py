from bs4 import BeautifulSoup, Comment
import hashlib

def getSoup(content):
    contentSoup = None
    try:
        contentSoup = BeautifulSoup(content, 'html.parser')
    except:
        print("There was an error converting content to soup")
    return contentSoup

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
                print('Could not extract link')
    return gamesLinks

def getTeamNames(gamePage):
    gamePageSoup = getSoup(gamePage)
    title = gamePageSoup.title.string
    teams = title.split(' - ')[0]
    away, home = teams.split(' at ')
    return home, away

def getStatTableDivs(gamePage):
    gamePageSoup = getSoup(gamePage)
    statTableDivs = None
    if gamePageSoup:
        statTableDivs = gamePageSoup.find_all('div', { 'class': 'table_wrapper'})
    return statTableDivs

def getTableByName(name, tables):
    return next((table for table in tables if table['id'] == name), None)

def getTableHeadAndBody(tableDiv):
    fullTable = tableDiv.find('table')

    tableHead = fullTable.find('thead')
    tableBody = fullTable.find('tbody')
    return tableHead, tableBody

def getBasicOverHeaderCounts(head):
    overheader = head.find_all('tr')[0].find_all('th')
    colCounts = [int(col['colspan']) for col in overheader]
    numInfo = colCounts[0]
    numPassing = sum(colCounts[:2])
    numRushing = sum(colCounts[:3])
    numReceiving = sum(colCounts[:4])
    numFumbles = sum(colCounts)
    return numInfo, numPassing, numRushing, numReceiving, numFumbles

def getStatKeys(head):
    stats = head.find_all('tr')[-1].find_all('th')
    statKeys = [stat.text.lower() for stat in stats]
    return statKeys

def getPlayerId(cell):
    atag = cell.find('a')
    link = atag['href']
    return hashlib.md5(link.encode()).hexdigest()

def findPlayerById(id, players):
    return next((player for player in players if player['player_id'] == id), None)

def convertStatIfNecessary(stat):
    if stat == '':
        stat = '0'
    stat = stat.replace('%', '')
    if stat.replace('.','',1).isnumeric():
        stat = float(stat)
        if stat.is_integer():
            stat = int(stat)
    return stat


def scrapeBasicOffense(head, body):
    # Absolutely YUUUUUGE function.  Could potentially break it down

    # This is a fat declaration
    numInfo, numPassing, numRushing, numReceiving, numFumbles = getBasicOverHeaderCounts(head)

    statKeys = getStatKeys(head)

    bodyRows = body.find_all('tr')
    offenseList = []
    for row in bodyRows:
        if not row.has_attr('class'):
            cells = row.find_all(recursive=False)
            player = {
                'info': {},
                'passing': {},
                'rushing': {},
                'receiving': {},
                'fumbles': {}
            }
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
                    print(f'Should never get here.\nstat: {stat}, value: {value}')
                count += 1
            offenseList.append(player)
    return offenseList

def getAdvancedTableFromComment(tableDiv):
    table = tableDiv.find(text=lambda text:isinstance(text, Comment))
    return BeautifulSoup(table, 'html.parser')

def scrapeAdvancedTable(head, body, statName, offenseList):
    statKeys = getStatKeys(head)

    rows = body.findAll('tr')
    for row in rows:
        if not row.has_attr('class'):
            count = 0
            statDict = {}
            playerID = None
            stats = row.findAll(recursive=False)

            for key, stat in zip(statKeys, stats):
                if count == 0:
                    playerID = getPlayerId(stat)
                if count < 2:
                    count += 1
                    continue

                value = convertStatIfNecessary(stat.text)
                statDict[key] = value
            player = findPlayerById(playerID, offenseList)
            player[statName] = statDict
