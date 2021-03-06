import requests
from bs4 import BeautifulSoup
import re

def makeWebScrapeRequest(url):
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )

    return r.content

def findElementsBeautifulSoup(soup, elementType, attribute, attributeValue):
    return soup.findAll(elementType,attrs={attribute : attributeValue}) 

def stripWhiteSpace(string):
    return string.strip()

def returnDateComponents(date):
    result = {}
    result['year'] = str(date)[0:4]
    result['month'] = str(date)[5:7]
    result['day'] = str(date)[8:10]
    return result

def returnStringDateRepresentation(date):
    return "{}-{}-{}".format(str(date)[0:4], str(date)[5:7], str(date)[8:10])

def validateDateQueryParameter(string):
    return re.match(r"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", string)

def validateNumberQueryParameter(number):
    return re.match(r"[0-9]", number)
