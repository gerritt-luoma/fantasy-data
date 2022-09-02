import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://www.pro-football-reference.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

def get(url: str) -> requests.Response:
    retval = None
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            retval = resp
        else:
            print("Response did not have a code of 200")
    except:
        print("Error fetching url")

    return retval

def getJSON(url: str):
    jsonVal = None
    resp = get(url)
    if resp != None:
        try:
            jsonVal = resp.json()
        except:
            print("Failure getting JSON")
    return jsonVal

def getContent(url: str):
    contentVal = None
    resp = get(url)
    if resp != None:
        contentVal = resp.content
    return contentVal

