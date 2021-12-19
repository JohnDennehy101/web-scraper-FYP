from bs4 import BeautifulSoup
from utils import findElementsBeautifulSoup, stripWhiteSpace

def returnScrapedFlightInformation(flightDepartureTime, flightArrivalTime, airportName, flightDuration, directFlightText, availableFlightPriceInfo):
    availableFlight = {
            "departureTime": stripWhiteSpace(flightDepartureTime.text),
            "arrivalTime": stripWhiteSpace(flightArrivalTime.text),
            "airport": stripWhiteSpace(airportName.text),
            "duration": stripWhiteSpace(flightDuration.text),
            "directFlight": stripWhiteSpace(directFlightText.text),
            "carrier": stripWhiteSpace(availableFlightPriceInfo["carrier"]),
            "pricePerPerson": stripWhiteSpace(availableFlightPriceInfo["pricePerPerson"]),
            "priceTotal": stripWhiteSpace(availableFlightPriceInfo["priceTotal"])
            }
    return availableFlight

def returnScrapedFlightPriceInfo(flightsCarrierName, flightsPricePerPerson, flightsPriceTotals):
    return {
        "carrier": stripWhiteSpace(flightsCarrierName.text),
        "pricePerPerson": stripWhiteSpace(flightsPricePerPerson.findChildren("span")[0].text),
        "priceTotal": stripWhiteSpace(flightsPriceTotals.text)
    }


def scrapeFlightInformation (data):
    soup = BeautifulSoup(data, 'html.parser')

    flightDepartureTimes = findElementsBeautifulSoup(soup,"span", "class", "depart-time base-time")

    flightArrivalTimes = findElementsBeautifulSoup(soup,"span", "class", "arrival-time base-time")

    airportNames = findElementsBeautifulSoup(soup,"span", "class", "airport-name")

    flightDurations = findElementsBeautifulSoup(soup,"div", "class", "section duration allow-multi-modal-icons")

    directFlightTexts = findElementsBeautifulSoup(soup,"span", "class", "stops-text")

    flightCarrierNames = findElementsBeautifulSoup(soup,"span", "class", "codeshares-airline-names")

    flightsPricePerPerson = findElementsBeautifulSoup(soup,"span", "class", "price option-text with-per-person-price")

    flightsPriceTotals = findElementsBeautifulSoup(soup,"div", "class", "price-total")

    flightGroup = []
    availableFlightsDict = {}
    availableFlightsDictIndex = 0
    for i in range(0, len(flightDepartureTimes)):

        if i % 2 == 0:
            index = int(i / 2)
            availableFlightPriceInfo = returnScrapedFlightPriceInfo(flightCarrierNames[index], flightsPricePerPerson[index], flightsPriceTotals[index])

            flightGroup.append((returnScrapedFlightInformation(flightDepartureTimes[i], flightArrivalTimes[i], airportNames[i], flightDurations[i], directFlightTexts[i], availableFlightPriceInfo)))

            if (len(flightGroup) > 1):
                availableFlightsDict[availableFlightsDictIndex] = flightGroup
                flightGroup = []
                availableFlightsDictIndex += 1
        else:
            flightGroup.append((returnScrapedFlightInformation(flightDepartureTimes[i], flightArrivalTimes[i], airportNames[i], flightDurations[i], directFlightTexts[i], availableFlightPriceInfo)))
    
    return availableFlightsDict