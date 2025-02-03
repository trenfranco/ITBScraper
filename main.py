from testProxy import test_proxy
from postScraper import postScraper
import re
import pandas as pd

def main():

    #these three are the different endpoint we need to scrape:
    #bussiness/travel entity_orga,cat_a0511318-3205-ee11-8f6e-000d3adf7d16
    #accomodations entity_orga,cat_30511318-3205-ee11-8f6e-000d3adf7d16
    #luxury entity_orga,cat_0e521318-3205-ee11-8f6e-000d3adf7d16

    url = "https://live.messebackend.aws.corussoft.de/webservice/search"
    data = {
        "topic": "2023_itb",
        "os": "web",
        "appUrl": "https://navigate.itb.com",
        "lang": "en",
        "apiVersion": 52,
        "timezoneOffset": 0,
        "numresultrows": 27,
        "startresultrow": 1,
        "filterlist": "entity_orga,cat_0e521318-3205-ee11-8f6e-000d3adf7d16",
        "order": "relevance",
        "secondaryOrder": "lexic",
        "desc": False
    }

    totalPages = int(input("Enter the number of total pages to scrape: "))
    i = 0
    offset = 1
    dictList = []

    while i < totalPages:
        dictList.extend(postScraper(url, data))
        offset = int(data["startresultrow"])
        offset += 27
        data["startresultrow"] = offset
        i+= 1

    df = pd.DataFrame(dictList)
    df.to_csv("Luxury.csv", index=False, encoding="utf-8")
    

if __name__ == "__main__":
    main()
    
