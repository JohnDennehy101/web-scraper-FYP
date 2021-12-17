import re
import requests

def requestAccommodationInformation(url):
    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )

    return r.content


def extractNumberOfAvailableProperties(numberOfAvailablePropertiesString):
    numberOfAvailablePropertiesRegexCheck = re.findall("[0-9]", numberOfAvailablePropertiesString)
    numberOfAvailableProperties = ''.join(numberOfAvailablePropertiesRegexCheck)
    print(numberOfAvailableProperties)
    return int(numberOfAvailableProperties)

def stripWhiteSpace(string):
    return string.strip()

def findElementsBeautifulSoup(soup, elementType, attribute):
    return soup.findAll(elementType,attrs={'data-testid' : attribute}) 
