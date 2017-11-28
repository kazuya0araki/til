# -*- coding:utf-8 -*-
import json
import csv
import pandas as pd
import config
from requests_oauthlib import OAuth1Session


CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)


# search
def search(url, keyword, count):
    params = {"q" : keyword, "count" : count}
    request = twitter.get(url, params=params)
    if request.status_code == 200:
        search_result = json.loads(request.text)
        fields = ["created_at", 'id', "text"]
        df = pd.DataFrame(search_result["statuses"], columns=fields)
        df.to_csv("result.csv", index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    else:
        print("ERROR: %d" % request.status_code)


if __name__ == '__main__':
    search(config.URL_SEARCH, config.SEARCH_KEYWORD, 100)
