import requests

# TODO: Add a headers object to my requests to mimic requests coming from a regular computer instead of a python request

def get(url: str) -> requests.Response:
    retval = None
    try:
        resp = requests.get(url)
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

