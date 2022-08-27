import json
import re
import requests

class RequestUtils:
    def get(self, url: str) -> requests.Response:
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

    def getJSON(self, url: str):
        jsonVal = None
        resp = self.get(url)
        if resp != None:
            try:
                jsonVal = resp.json()
            except:
                print("Failure getting JSON")
        return jsonVal

    def getContent(self, url: str):
        contentVal = None
        resp = self.get(url)
        if resp != None:
            try:
                contentVal = resp.content
            except:
                print("Failure getting content")
        return contentVal

