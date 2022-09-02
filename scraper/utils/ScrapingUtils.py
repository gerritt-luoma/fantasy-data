from bs4 import BeautifulSoup, Comment

def getSoup(content):
    contentSoup = None
    try:
        contentSoup = BeautifulSoup(content, 'html.parser')
    except:
        print("There was an error converting content to soup")
    return contentSoup

def getWeeklyGames(gamesPage):
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

def getStatTables(gamePage):
    gamePageSoup = getSoup(gamePage)
    statTables = None
    if gamePageSoup:
        statTables = gamePageSoup.find_all('div', { 'class': 'table_wrapper'})
    return statTables

def getTableByName(name, tables):
    return next((table for table in tables if table['id'] == name), None)