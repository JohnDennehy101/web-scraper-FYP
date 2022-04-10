import re
from bs4 import BeautifulSoup
from utils import findElementsBeautifulSoup, stripWhiteSpace
from database import insertAccommodationInfo

def extractNumberOfAvailableProperties(numberOfAvailablePropertiesString):
    numberOfAvailablePropertiesRegexCheck = re.findall("[0-9]", numberOfAvailablePropertiesString)
    numberOfAvailableProperties = ''.join(numberOfAvailablePropertiesRegexCheck)
    return int(numberOfAvailableProperties)

def returnScrapedHotelInformation(hotelName, bookingSiteLink, bookingSiteLocationLink, bookingSiteLocationText, bookingSiteDistance, bookingSiteReviews, bookingSiteAvailabilityGroup, bookingSiteAvailabilitySingle, bookingSiteRoomNightAvailability, bookingSitePrice, bookingSiteRoomLink, i):

    availableProperty = None

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


    availableProperty = {
            "title": stripWhiteSpace(hotelName.text),
            "bookingSiteLink": stripWhiteSpace(bookingSiteLink['href']),
            "bookingSiteDisplayLocationMapLink": stripWhiteSpace(bookingSiteLocationLink.findChildren("a")[0]['href']),
            "locationTitle": stripWhiteSpace(bookingSiteLocationText.text),
            "locationDistance": stripWhiteSpace(bookingSiteDistance.text),
            "ratingScore": stripWhiteSpace(ratingScore),
            "ratingScoreCategory": stripWhiteSpace(ratingScoreCategory),
            "reviewQuantity": stripWhiteSpace(reviewQuantity),
            "numberOfRoomsRecommendedBooking": stripWhiteSpace(numberOfRoomsRecommendedBooking),
            "roomTypeRecommendedBooking": stripWhiteSpace(roomTypeRecommendedBooking),
            "numberOfBedsRecommendedBooking": stripWhiteSpace(numberOfBedsRecommendedBooking),
            "freeCancellationText": stripWhiteSpace(freeCancellationText),
            "numberOfNightsAndGuests": stripWhiteSpace(bookingSiteRoomNightAvailability.text),
            "price": stripWhiteSpace(bookingSitePrice.findChildren("span")[0].text),
            "bookingPreviewLink": stripWhiteSpace(bookingSiteRoomLink.findChildren("a")[0]['href'])
        }
    return availableProperty



def scrapeHotelInformation (data):
    soup = BeautifulSoup(data, 'html.parser')

    numberOfProperties = soup.findAll("div", attrs={'data-component': 'arp-header'})[0].findChildren("h1")[0].text

    hotelNames = findElementsBeautifulSoup(soup,"div", "data-testid", "title")

    bookingSiteLinks = findElementsBeautifulSoup(soup,"a", "data-testid", "title-link")

    bookingSiteLocationLinks = findElementsBeautifulSoup(soup,"div", "data-testid", "location")
 
    bookingSiteLocationTexts = findElementsBeautifulSoup(soup,"span", "data-testid", "address")

    bookingSiteDistances = findElementsBeautifulSoup(soup,"span", "data-testid", "distance")

    bookingSiteReviews = findElementsBeautifulSoup(soup,"div", "data-testid", "review-score")

    bookingSiteAvailabilityGroup = findElementsBeautifulSoup(soup, "div", "data-testid", "availability-group")

    bookingSiteAvailabilitySingle = findElementsBeautifulSoup(soup,"div", "data-testid", "availability-single")

    bookingSiteRoomNightAvailability = findElementsBeautifulSoup(soup,"div", "data-testid", "price-for-x-nights")
 
    bookingSitePrices = findElementsBeautifulSoup(soup,"div", "data-testid", "price-and-discounted-price")
 
    bookingSiteRoomLink = findElementsBeautifulSoup(soup,"div", "data-testid", "availability-cta")
    
    availablePropertiesArray = []
    for i in range(0, len(hotelNames)):

        availablePropertiesArray.append(returnScrapedHotelInformation(hotelNames[i],bookingSiteLinks[i],bookingSiteLocationLinks[i],bookingSiteLocationTexts[i],bookingSiteDistances[i],bookingSiteReviews,bookingSiteAvailabilityGroup,bookingSiteAvailabilitySingle,bookingSiteRoomNightAvailability[i],bookingSitePrices[i],bookingSiteRoomLink[i], i))

    return {
        "propertiesResult": availablePropertiesArray,
        "numberOfPropertiesString": numberOfProperties
    }
