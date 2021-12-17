from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
import time
from pprint import pprint
import re
from random import randint
from time import sleep



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
#html = requestAccommodationInformation(url)

test = {
        "propertiesResult": [],
        "offset": 0,
        "numberOfPropertiesString": "Dublin: 186 properties found"
    }

#numberofAvailableProperties = extractNumberOfAvailableProperties(test['numberOfPropertiesString'])

"""
r = requests.get(
        "https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=Dublin&is_ski_area=0&ssne=Dublin&ssne_untouched=Dublin&dest_id=-1502554&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=26&checkout_year=2022&checkout_month=1&checkout_monthday=29&group_adults=5&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )

html = r.content
"""



def stripWhiteSpace (string):
    return string.strip()


def checkAvailableNode (node):
    try:
        return node
    except IndexError:
        return default



def scrapeHotelInformation (data, offset):
    soup = BeautifulSoup(data, 'html.parser')

    with open("dublin_booking_5.com.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))
    


    #Find number of properties available (use this to loop over different pages of results)
    numberOfProperties = soup.findAll("div", attrs={'data-component': 'arp-header'})[0].findChildren("h1")[0].text


    hotelNames = soup.findAll("div",attrs={'data-testid' : 'title'}) 
    bookingSiteLinks = soup.findAll("a", attrs={'data-testid': 'title-link'})
    bookingSiteLocationLinks = soup.findAll("div", attrs={'data-testid': 'location'})
    bookingSiteLocationTexts = soup.findAll("span", attrs={'data-testid': 'address'})
    bookingSiteDistances = soup.findAll("span", attrs={'data-testid': 'distance'})
    bookingSiteReviews = soup.findAll("div", attrs={'data-testid': 'review-score'})
    bookingSiteAvailabilityGroup = soup.findAll("div", attrs={'data-testid': 'availability-group'})
    bookingSiteAvailabilitySingle = soup.findAll("div", attrs={'data-testid': 'availability-single'})
    bookingSiteRoomNightAvailability = soup.findAll("div", attrs={'data-testid': 'price-for-x-nights'})
    bookingSitePrices = soup.findAll("div", attrs={'data-testid': 'price-and-discounted-price'})
    bookingSiteRoomLink = soup.findAll("div", attrs={'data-testid' : 'availability-cta'})

    availablePropertiesArray = []
    
    

    for i in range(0, len(hotelNames)):


        ratingScore = None
        ratingScoreCategory = None
        reviewQuantity = None
        bookingSiteAvailabilityType = None

        if i < len(bookingSiteReviews):


            if len(bookingSiteReviews[i].findChildren("div")) > 3:
                reviewQuantity = bookingSiteReviews[i].findChildren("div")[3].text

            else:
                reviewQuantity = "Review Quantity Information Not Available"


            if len(bookingSiteReviews[i].findChildren("div")) > 2:
                ratingScoreCategory = bookingSiteReviews[i].findChildren("div")[2].text

            else:
                ratingScoreCategory = "Rating Score Category Not Available"

            if bookingSiteReviews[i].findChildren("div"):
                ratingScore = bookingSiteReviews[i].findChildren("div")[0].text

            else:
                ratingScore = "Rating Score Not Available"

        else:
            reviewQuantity = "Review Quantity Information Not Available"
            ratingScore = "Rating Score Not Available"
            ratingScoreCategory = "Rating Score Category Not Available"

       
        if len(bookingSiteAvailabilityGroup) > 0:
            bookingSiteAvailabilityType = bookingSiteAvailabilityGroup[i]
            if bookingSiteAvailabilityGroup[i].findChildren("div")[1]:
            
                freeCancellationText = None
                roomTypeRecommendedBooking = None
                numberOfBedsRecommendedBooking = None
                if len(bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("div")) > 6:
                    freeCancellationText = bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("div")[6].text
                else:
                    freeCancellationText = "Free Cancellation Not Available"

            
                print("CHECKING HERE")
                print(bookingSiteAvailabilityGroup[i].findChildren("span")[0])
            
                if len(bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("span")) > 3:
                    roomTypeRecommendedBooking = bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("span")[3].text
                else:
                    roomTypeRecommendedBooking = "Recommended Booking Room Type Info Not Available"
            
                if len(bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("div")) > 4:
                    numberOfBedsRecommendedBooking = bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("div")[4].text
                else:
                    numberOfBedsRecommendedBooking = "Recommended Booking Info Not Available"

        elif len(bookingSiteAvailabilitySingle) > 0:
             print("HITTING Booking Single Type")
             bookingSiteAvailabilityType = bookingSiteAvailabilitySingle[i]
             if bookingSiteAvailabilitySingle[i].findChildren("div")[1]:
            
                freeCancellationText = None
                roomTypeRecommendedBooking = None
                numberOfBedsRecommendedBooking = None
                if len(bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")) >= 7:
                    freeCancellationText = bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")[6].text
                else:
                    freeCancellationText = "Free Cancellation Not Available"

            
                print("BEFORE CHEDCK")
                print(bookingSiteAvailabilitySingle[i].findChildren("span")[0].text)
                if len(bookingSiteAvailabilitySingle[i].findChildren("span")) > 0:
                    print("ARE WEE THERE")
                    roomTypeRecommendedBooking = bookingSiteAvailabilitySingle[i].findChildren("span")[0].text
                else:
                    roomTypeRecommendedBooking = "Recommended Booking Room Type Info Not Available"
            
                if len(bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")) >= 5:
                    numberOfBedsRecommendedBooking = bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")[4].text
                else:
                    numberOfBedsRecommendedBooking = "Recommended Booking Info Not Available"


        availablePropertiesArray.append({
            "title": stripWhiteSpace(hotelNames[i].text),
            "bookingSiteLink": stripWhiteSpace(bookingSiteLinks[i]['href']),
            "bookingSiteDisplayLocationMapLink": stripWhiteSpace(bookingSiteLocationLinks[i].findChildren("a")[0]['href']),
            "locationTitle": stripWhiteSpace(bookingSiteLocationTexts[i].text),
            "locationDistance": stripWhiteSpace(bookingSiteDistances[i].text),
            "ratingScore": stripWhiteSpace(ratingScore),
            "ratingScoreCategory": stripWhiteSpace(ratingScoreCategory),
            "reviewQuantity": stripWhiteSpace(reviewQuantity),
            #"numberOfRoomsRecommendedBooking": stripWhiteSpace(bookingSiteAvailabilityType.findChildren("div")[1].findChildren("span")[2].text),
            "numberOfRoomsRecommendedBooking": stripWhiteSpace(bookingSiteAvailabilityType.findChildren("span")[0].text),
            "roomTypeRecommendedBooking": stripWhiteSpace(roomTypeRecommendedBooking),
            "numberOfBedsRecommendedBooking": stripWhiteSpace(numberOfBedsRecommendedBooking),
            "freeCancellationText": stripWhiteSpace(freeCancellationText),
            "numberOfNightsAndGuests": stripWhiteSpace(bookingSiteRoomNightAvailability[i].text),
            "price": stripWhiteSpace(bookingSitePrices[i].findChildren("span")[0].text),
            "bookingPreviewLink": stripWhiteSpace(bookingSiteRoomLink[i].findChildren("a")[0]['href'])
        })
    
    #pprint(availablePropertiesArray)

    return {
        "propertiesResult": availablePropertiesArray,
        "offset": offset,
        "numberOfPropertiesString": numberOfProperties
    }


additionalPage = True
offset = 0
offsetQueryParameter = ''
finalCheckArray = []

while additionalPage:
    url = "https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=Dublin&is_ski_area=0&ssne=Dublin&ssne_untouched=Dublin&dest_id=-1502554&dest_type=city&checkin_year=2022&checkin_month=4&checkin_monthday=6&checkout_year=2022&checkout_month=4&checkout_monthday=8&group_adults=5&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1"
    if offset > 0:
        offsetQueryParameter = "&offset={quantity}".format(quantity=offset)
        url += offsetQueryParameter
    

    print(url)
    print(offset)
    #html = None
    html = requestAccommodationInformation(url)
    
    #with open('limerick_booking.com.html', 'r') as f:
     #   contents = f.read()
     #   html = contents
        
       
    sleep(randint(5,15))
    resultDict = scrapeHotelInformation(html, offset) 
    finalCheckArray.append(resultDict['propertiesResult'])
    numberOfProperties = extractNumberOfAvailableProperties(resultDict['numberOfPropertiesString'])
    offset += 25
    #if (numberOfProperties - offset) < 0:
    if offset == 50:
        additionalPage = False
    #additionalPage = False
     


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


