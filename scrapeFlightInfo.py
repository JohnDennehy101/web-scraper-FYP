from bs4 import BeautifulSoup
from utils import findElementsBeautifulSoup, stripWhiteSpace

def returnScrapedFlightInformation(flightDepartureTime, flightArrivalTime, airportName, flightDuration, directFlightText, availableFlightPriceInfo):
    availableFlight = {
            "departureTime": stripWhiteSpace(flightDepartureTime.text),
            "arrivalTime": stripWhiteSpace(flightArrivalTime.text),
            "airport": stripWhiteSpace(airportName.text),
            "duration": stripWhiteSpace(flightDuration.find("div", {"class": "top"}).text),
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

    with open("dublin_london_kayak_attempt_3.com.html", "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))

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
            try:
                if index < len(flightCarrierNames) and index < len(flightsPricePerPerson) and index < len(flightsPriceTotals):
                    availableFlightPriceInfo = returnScrapedFlightPriceInfo(flightCarrierNames[index], flightsPricePerPerson[index], flightsPriceTotals[index])

                    flightGroup.append((returnScrapedFlightInformation(flightDepartureTimes[i], flightArrivalTimes[i], airportNames[i], flightDurations[i], directFlightTexts[i], availableFlightPriceInfo)))
            except:
                raise Exception("Error adding flight result. Out of range.")

            if (len(flightGroup) > 1):
                if availableFlightsDictIndex is 0:
                    availableFlightsDict[availableFlightsDictIndex] = flightGroup
                else:
                    print("HITTING")
                    departureAirport = flightGroup[1]["airport"]
                    arrivalAirport = flightGroup[0]["airport"]
                    flightGroup[0]["airport"] = departureAirport
                    flightGroup[1]["airport"] = arrivalAirport
                    availableFlightsDict[availableFlightsDictIndex] = flightGroup
                    print(flightGroup)
                flightGroup = []
                availableFlightsDictIndex += 1
        else:
            index = int(i / 2)

            try:
                if index < len(flightCarrierNames) and index < len(flightsPricePerPerson) and index < len(flightsPriceTotals):
                    availableFlightPriceInfo = returnScrapedFlightPriceInfo(flightCarrierNames[index], flightsPricePerPerson[index], flightsPriceTotals[index])
                    flightGroup.append((returnScrapedFlightInformation(flightDepartureTimes[i], flightArrivalTimes[i], airportNames[i], flightDurations[i], directFlightTexts[i], availableFlightPriceInfo)))
            except:
                raise Exception("Error adding flight result. Out of range.")

            if (len(flightGroup) > 1):
                if availableFlightsDictIndex is 0:
                    availableFlightsDict[availableFlightsDictIndex] = flightGroup
                else:
                    print("HITTING")
                    departureAirport = flightGroup[1]["airport"]
                    arrivalAirport = flightGroup[0]["airport"]
                    flightGroup[0]["airport"] = departureAirport
                    flightGroup[1]["airport"] = arrivalAirport
                    availableFlightsDict[availableFlightsDictIndex] = flightGroup
                    print(flightGroup)
                flightGroup = []
                availableFlightsDictIndex += 1
    
    return availableFlightsDict