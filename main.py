from dotenv import load_dotenv
import os
import time
from pprint import pprint
from random import randint
from time import sleep
from scrapeAccommodationInfo import extractNumberOfAvailableProperties, stripWhiteSpace, findElementsBeautifulSoup, scrapeHotelInformation, returnScrapedHotelInformation
from scrapeFlightInfo import scrapeFlightInformation
from utils import makeWebScrapeRequest

additionalPage = True
offset = 0
offsetQueryParameter = ''
finalCheckArray = []

while additionalPage:
    hotelSiteUrl = "https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=Kilkenny&is_ski_area=0&ssne=Kilkenny&ssne_untouched=Kilkenny&dest_id=-1503733&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=14&checkout_year=2022&checkout_month=1&checkout_monthday=15&group_adults=6&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1"
    flightSiteUrl = "https://www.kayak.ie/flights/DUB-LON/2022-01-16/2022-01-23/3adults?sort=bestflight_a"
    if offset > 0:
        offsetQueryParameter = "&offset={quantity}".format(quantity=offset)
        hotelSiteUrl += offsetQueryParameter
    

    print(hotelSiteUrl)
    print(offset)
    hotelHtml = None
    #flightHtml = makeWebScrapeRequest(flightSiteUrl)
    #hotelHtml = makeWebScrapeRequest(hotelSiteUrl)
    flighHtml = None

    
    
    with open('limerick_booking.com.html', 'r') as f:
        contents = f.read()
        hotelHtml = contents
    
    with open('dublin_london_kayak.com.html', 'r') as f:
        contents = f.read()
        flightHtml = contents
        
    scrapeFlightInformation(flightHtml, offset)  
    #sleep(randint(5,15))
    resultDict = scrapeHotelInformation(hotelHtml, offset) 
    finalCheckArray.append(resultDict['propertiesResult'])
    numberOfProperties = extractNumberOfAvailableProperties(resultDict['numberOfPropertiesString'])
    offset += 25
    #if (numberOfProperties - offset) < 0:
    if offset == 50:
        additionalPage = False
    additionalPage = False
     


#print(finalCheckArray)
with open("results.txt", "w") as file:
    file.write(str(finalCheckArray))

"""
with open('dublin_booking.com.html', 'r') as f:

    contents = f.read()
    #html = r.content
    html = contents
    scrapeHotelInformation(html)     
"""


