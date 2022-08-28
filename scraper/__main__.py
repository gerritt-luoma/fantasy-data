import utils.requestUtils as ru

if __name__ == '__main__':
    requestHelper = ru.RequestUtils()
    content = requestHelper.getContent('https://www.pro-football-reference.com/years/2021/week_1.htm')
    