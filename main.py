from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
from pprint import pprint
from random import randint
from time import sleep
from scrapeAccommodationInfo import requestAccommodationInformation, extractNumberOfAvailableProperties, stripWhiteSpace, findElementsBeautifulSoup



def scrapeHotelInformation (data, offset):
    soup = BeautifulSoup(data, 'html.parser')

    #with open("kilkenny_booking_6.com.html", "w", encoding='utf-8') as file:
    #   file.write(str(soup.prettify()))

    
    
    #Find number of properties available (use this to loop over different pages of results)
    numberOfProperties = soup.findAll("div", attrs={'data-component': 'arp-header'})[0].findChildren("h1")[0].text


    hotelNames = findElementsBeautifulSoup(soup,"div", "title")

    bookingSiteLinks = findElementsBeautifulSoup(soup,"a", "title-link")

    bookingSiteLocationLinks = findElementsBeautifulSoup(soup,"div", "location")
 
    bookingSiteLocationTexts = findElementsBeautifulSoup(soup,"span", "address")

    bookingSiteDistances = findElementsBeautifulSoup(soup,"span", "distance")

    bookingSiteReviews = findElementsBeautifulSoup(soup,"div", "review-score")

    bookingSiteAvailabilityGroup = findElementsBeautifulSoup(soup, "div", "availability-group")

    bookingSiteAvailabilitySingle = findElementsBeautifulSoup(soup,"div", "availability-single")

    bookingSiteRoomNightAvailability = findElementsBeautifulSoup(soup,"div", "price-for-x-nights")
 
    bookingSitePrices = findElementsBeautifulSoup(soup,"div", "price-and-discounted-price")
 
    bookingSiteRoomLink = findElementsBeautifulSoup(soup,"div", "availability-cta")

    availablePropertiesArray = []
    
    

    for i in range(0, len(hotelNames)):


        ratingScore = None
        ratingScoreCategory = None
        reviewQuantity = None
        bookingSiteAvailabilityType = None
        numberOfRoomsRecommendedBooking = None

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

            
            
                if len(bookingSiteAvailabilityGroup[i].findChildren("div")[1].findChildren("span")) > 3:
                    roomTypeRecommendedBooking = bookingSiteAvailabilityGroup[i].findChildren("span")[3].text
                    numberOfRoomsRecommendedBooking = bookingSiteAvailabilityGroup[i].findChildren("span")[2].text
                else:
                    roomTypeRecommendedBooking = "Recommended Booking Room Type Info Not Available"
                    numberOfRoomsRecommendedBooking = "Number of Rooms Info Not Available"
            
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
                numberOfRoomsRecommendedBooking = bookingSiteAvailabilitySingle[i].findChildren("span")[0].text
                if len(bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")) >= 7:
                    freeCancellationText = bookingSiteAvailabilitySingle[i].findChildren("div")[1].findChildren("div")[6].text
                else:
                    freeCancellationText = "Free Cancellation Not Available"

            
              
                if len(bookingSiteAvailabilitySingle[i].findChildren("span")) > 0:
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
            "numberOfRoomsRecommendedBooking": stripWhiteSpace(numberOfRoomsRecommendedBooking),
            "roomTypeRecommendedBooking": stripWhiteSpace(roomTypeRecommendedBooking),
            "numberOfBedsRecommendedBooking": stripWhiteSpace(numberOfBedsRecommendedBooking),
            "freeCancellationText": stripWhiteSpace(freeCancellationText),
            "numberOfNightsAndGuests": stripWhiteSpace(bookingSiteRoomNightAvailability[i].text),
            "price": stripWhiteSpace(bookingSitePrices[i].findChildren("span")[0].text),
            "bookingPreviewLink": stripWhiteSpace(bookingSiteRoomLink[i].findChildren("a")[0]['href'])
        })

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
    url = "https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=Kilkenny&is_ski_area=0&ssne=Kilkenny&ssne_untouched=Kilkenny&dest_id=-1503733&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=14&checkout_year=2022&checkout_month=1&checkout_monthday=15&group_adults=6&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1"
    if offset > 0:
        offsetQueryParameter = "&offset={quantity}".format(quantity=offset)
        url += offsetQueryParameter
    

    print(url)
    print(offset)
    html = None
    #html = requestAccommodationInformation(url)
    
    with open('limerick_booking.com.html', 'r') as f:
        contents = f.read()
        html = contents
        
       
    #sleep(randint(5,15))
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


