from bs4 import BeautifulSoup

def scrapeFlightInformation (data, offset):
    soup = BeautifulSoup(data, 'html.parser')

    flightResultsParentContainer = soup.findAll('div', attrs={"class": "best-flights-list-results"})

    flightDepartureTimes = soup.findAll('span', attrs={"class": "depart-time base-time"})

    flightArrivalTimes = soup.findAll('span', attrs={"class": "arrival-time base-time"})

    airportNames = soup.findAll('span', attrs={"class": "airport-name"})

    #Loop in each flightDurations[i].findChildren("div")[0]
    flightDurations = soup.findAll('div', attrs={"class": "section duration allow-multi-modal-icons"})

    directFlightTexts = soup.findAll('span', attrs={"class": "stops-text"})

    flightCarrierNames = soup.findAll('span', attrs={"class": "codeshares-airline-names"})

    #Loop in each to get price per person (will need to join 2 strings) flightsPricePerPerson[0].findChildren('span')[0] & flightsPricePerPerson[0].findChildren('span')[1] 
    flightsPricePerPerson = soup.findAll('span', attrs={"class": "price option-text with-per-person-price"})

    flightsPriceTotals = soup.findAll('div', attrs={"class": "price-total"})


    for item in flightsPricePerPerson:
        print(item)

    

    #with open("dublin_london_kayak.com.html", "w", encoding='utf-8') as file:
    #   file.write(str(soup.prettify()))