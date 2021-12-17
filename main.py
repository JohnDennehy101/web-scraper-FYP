from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
import time
from pprint import pprint



r = requests.get(
        "https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=Dublin&is_ski_area=0&ssne=Dublin&ssne_untouched=Dublin&dest_id=-1502554&dest_type=city&checkin_year=2022&checkin_month=1&checkin_monthday=26&checkout_year=2022&checkout_month=1&checkout_monthday=29&group_adults=5&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0)"
            " Gecko/20100101 Firefox/48.0"
        },
    )

html = r.content



def stripWhiteSpace (string):
    return string.strip()


def checkAvailableNode (node):
    try:
        return node
    except IndexError:
        return default



def scrapeHotelInformation (data):
    soup = BeautifulSoup(data, 'html.parser')

    #with open("dublin_booking.com.html", "w", encoding='utf-8') as file:
     #   file.write(str(soup.prettify()))

    #Find number of properties available (use this to loop over different pages of results)
    numberOfProperties = soup.findAll("div", attrs={'data-component': 'arp-header'})[0].findChildren("h1")[0].text

    print(numberOfProperties)

    hotelNames = soup.findAll("div",attrs={'data-testid' : 'title'}) 
    bookingSiteLinks = soup.findAll("a", attrs={'data-testid': 'title-link'})
    bookingSiteLocationLinks = soup.findAll("div", attrs={'data-testid': 'location'})
    bookingSiteLocationTexts = soup.findAll("span", attrs={'data-testid': 'address'})
    bookingSiteDistances = soup.findAll("span", attrs={'data-testid': 'distance'})
    bookingSiteReviews = soup.findAll("div", attrs={'data-testid': 'review-score'})
    bookingSiteAvailability = soup.findAll("div", attrs={'data-testid': 'availability-group'})
    bookingSiteRoomNightAvailability = soup.findAll("div", attrs={'data-testid': 'price-for-x-nights'})
    bookingSitePrices = soup.findAll("div", attrs={'data-testid': 'price-and-discounted-price'})
    bookingSiteRoomLink = soup.findAll("div", attrs={'data-testid' : 'availability-cta'})

    availablePropertiesArray = []
    
    

    for i in range(0, len(hotelNames)):


        ratingScore = None
        ratingScoreCategory = None
        reviewQuantity = None

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

        if bookingSiteAvailability[i].findChildren("div")[1]:
            
            freeCancellationText = None
            roomTypeRecommendedBooking = None
            numberOfBedsRecommendedBooking = None
            if len(bookingSiteAvailability[i].findChildren("div")[1].findChildren("div")) > 6:
                freeCancellationText = bookingSiteAvailability[i].findChildren("div")[1].findChildren("div")[6].text
            else:
                freeCancellationText = "Free Cancellation Not Available"

            
            if len(bookingSiteAvailability[i].findChildren("div")[1].findChildren("span")) > 3:
                roomTypeRecommendedBooking = bookingSiteAvailability[i].findChildren("div")[1].findChildren("span")[3].text
            else:
                roomTypeRecommendedBooking = "Recommended Booking Room Type Info Not Available"
            
            if len(bookingSiteAvailability[i].findChildren("div")[1].findChildren("div")) > 4:
                numberOfBedsRecommendedBooking = bookingSiteAvailability[i].findChildren("div")[1].findChildren("div")[4].text
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
            "numberOfRoomsRecommendedBooking": stripWhiteSpace(bookingSiteAvailability[i].findChildren("div")[1].findChildren("span")[2].text),
            "roomTypeRecommendedBooking": stripWhiteSpace(roomTypeRecommendedBooking),
            "numberOfBedsRecommendedBooking": stripWhiteSpace(numberOfBedsRecommendedBooking),
            "freeCancellationText": stripWhiteSpace(freeCancellationText),
            "numberOfNightsAndGuests": stripWhiteSpace(bookingSiteRoomNightAvailability[i].text),
            "price": stripWhiteSpace(bookingSitePrices[i].findChildren("span")[0].text),
            "bookingPreviewLink": stripWhiteSpace(bookingSiteRoomLink[i].findChildren("a")[0]['href'])
        })
    
    pprint(availablePropertiesArray)


scrapeHotelInformation(html) 
        

"""
with open('dublin_booking.com.html', 'r') as f:

    contents = f.read()
    #html = r.content
    html = contents
    scrapeHotelInformation(html)     
"""


