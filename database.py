from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os
import datetime
from utils import returnStringDateRepresentation

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_NAME = os.getenv("DB_NAME")

def createDbConnection(hostName, userName, userPassword, dbName):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostName,
            user=userName,
            passwd=userPassword,
            database=dbName
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def bootstrapDbOnInitialLoad():
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    
    print(connection)

    createDatabaseQuery = "CREATE DATABASE {databaseName}".format(databaseName=DB_NAME)

    createFlightTable = """
    CREATE TABLE flight (
    flightId int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (flightId),
    startDate VARCHAR (100),
    endDate VARCHAR (100),
    departureCity VARCHAR(100),
    arrivalCity VARCHAR(100),
    departureTime VARCHAR(100) NOT NULL,
    arrivalTime VARCHAR(100) NOT NULL,
    airport VARCHAR(100),
    duration VARCHAR(100),
    directFlight VARCHAR(100),
    carrier VARCHAR(200),
    pricePerPerson VARCHAR(100),
    priceTotal VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    indexPosition VARCHAR(10),
    flightUrl VARCHAR(500)
    );
    """

    createAccommodationTable = """
    CREATE TABLE accommodation (
    accommodationId int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (accommodationId),
    startDate VARCHAR (100),
    endDate VARCHAR (100),
    title VARCHAR(200) NOT NULL,
    bookingPreviewLink VARCHAR(700),
    bookingSiteDisplayLocationMapLink VARCHAR(700),
    bookingSiteLink VARCHAR(700),
    freeCancellationText VARCHAR(200),
    locationDistance VARCHAR(100),
    locationTitle VARCHAR(100),
    numberOfBedsRecommendedBooking VARCHAR(700),
    numberOfNightsAndGuests VARCHAR(300),
    numberOfRoomsRecommendedBooking VARCHAR(300),
    price VARCHAR(50),
    ratingScore VARCHAR(50),
    ratingScoreCategory VARCHAR(50),
    reviewQuantity VARCHAR(50),
    roomTypeRecommendedBooking VARCHAR(50),
    page VARCHAR(5),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    createDb(connection, createDatabaseQuery)
    executeQuery(connection, createAccommodationTable)
    executeQuery(connection, createFlightTable)

    


def createDb(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def executeListQuery(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def insertAccommodationInfo(accommodationList, page, startDate, endDate):
    accommodationInfoForDbInsertion = []
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    for i in range(0, len(accommodationList)):
        individualItem = (startDateString, endDateString, accommodationList[i]["title"], accommodationList[i]["bookingPreviewLink"], accommodationList[i]["bookingSiteDisplayLocationMapLink"], accommodationList[i]["bookingSiteLink"], accommodationList[i]["freeCancellationText"], accommodationList[i]["locationDistance"], accommodationList[i]["locationTitle"], accommodationList[i]["numberOfBedsRecommendedBooking"], accommodationList[i]["numberOfNightsAndGuests"], accommodationList[i]["numberOfRoomsRecommendedBooking"], accommodationList[i]["price"], accommodationList[i]["ratingScore"], accommodationList[i]["ratingScoreCategory"], accommodationList[i]["reviewQuantity"], accommodationList[i]["roomTypeRecommendedBooking"], str(page))
        accommodationInfoForDbInsertion.append(individualItem)
    

    insertAccommodationQuery = """
    INSERT INTO accommodation (startDate, endDate, title, bookingPreviewLink, bookingSiteDisplayLocationMapLink, bookingSiteLink, freeCancellationText, locationDistance, locationTitle, numberOfBedsRecommendedBooking, numberOfNightsAndGuests, numberOfRoomsRecommendedBooking, price, ratingScore, ratingScoreCategory, reviewQuantity, roomTypeRecommendedBooking, page) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    executeListQuery(connection, insertAccommodationQuery, accommodationInfoForDbInsertion)
    

def insertFlightInfo(flightList, startDate, endDate, fromCity, destinationCity, completeFlightUrl):
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    flightInfoForDbInsertion = []
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)

    for listKey in range(0,len(flightList.keys())):
        for i in range(0, len(flightList[listKey])):
            individualItem = (startDateString, endDateString, fromCity, destinationCity, flightList[listKey][i]["departureTime"], flightList[listKey][i]["arrivalTime"], flightList[listKey][i]["airport"], flightList[listKey][i]["duration"], flightList[listKey][i]["directFlight"], flightList[listKey][i]["carrier"], flightList[listKey][i]["pricePerPerson"], flightList[listKey][i]["priceTotal"], listKey, completeFlightUrl)
            flightInfoForDbInsertion.append(individualItem)


    insertFlightQuery = """
    INSERT INTO flight (startDate, endDate, departureCity, arrivalCity, departureTime, arrivalTime, airport, duration, directFlight, carrier, pricePerPerson, priceTotal, indexPosition, flightUrl) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    executeListQuery(connection, insertFlightQuery, flightInfoForDbInsertion)


def checkDbForExistingRecords(destinationCity, startDate, endDate):
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)

    timestampMinusADay = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    existingRecordsQuery = """
    SELECT * FROM accommodation
    WHERE locationTitle LIKE '{}' AND startDate = '{}' AND endDate = '{}' AND timestamp > '{}'
    """.format("%" + destinationCity + "%", startDateString, endDateString, timestampMinusADay)

    

    dbRecords = readQuery(connection, existingRecordsQuery)

    if dbRecords:


        if len(dbRecords) > 0:

            result = {"resultPages": {
            "1": [],
            "2": [],
            "3": []
        }}
            print(len(dbRecords))

            for record in range(len(dbRecords)):
           
                individualRecord = list(dbRecords[record])
                page = individualRecord[18]

                result["resultPages"][page].append({
                "title": individualRecord[3],
                "startDate": individualRecord[1],
                "endDate": individualRecord[2],
                "bookingSiteLink": individualRecord[6],
                "bookingSiteDisplayLocationMapLink": individualRecord[5],
                "locationTitle": individualRecord[9],
                "locationDistance": individualRecord[8],
                "ratingScore": individualRecord[14],
                "ratingScoreCategory": individualRecord[15],
                "reviewQuantity": individualRecord[16],
                "numberOfRoomsRecommendedBooking": individualRecord[12],
                "roomTypeRecommendedBooking": individualRecord[17],
                "numberOfBedsRecommendedBooking": individualRecord[10],
                "freeCancellationText": individualRecord[7],
                "numberOfNightsAndGuests": individualRecord[11],
                "price": individualRecord[13],
                "bookingPreviewLink": individualRecord[4] 
            })
            
            for page in result["resultPages"].copy():
                if len(result["resultPages"][page]) == 0:
                    del result["resultPages"][page]

            return result

        else:
            return []



def checkDbForExistingFlightRecords(fromCity, destinationCity, startDate, endDate):
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)

    timestampMinusADay = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    existingRecordsQuery = """
    SELECT * FROM flight
    WHERE departureCity = '{}' AND arrivalCity = '{}' AND startDate = '{}' AND endDate = '{}' AND timestamp > '{}'
    ORDER BY indexPosition
    """.format(fromCity, destinationCity, startDateString, endDateString, timestampMinusADay)

    

    dbRecords = readQuery(connection, existingRecordsQuery)

    if dbRecords is not None:

        if len(dbRecords) > 0:

            result = []


            for record in range(len(dbRecords)):
           
                individualRecord = list(dbRecords[record])

                result.append({
                "startDate": individualRecord[1],
                "endDate": individualRecord[2],
                "departureTime": individualRecord[5],
                "departureCity": individualRecord[3] ,
                "arrivalCity": individualRecord[4],
                "arrivalTime": individualRecord[6],
                "airport": individualRecord[7],
                "duration": individualRecord[8],
                "directFlight": individualRecord[9],
                "carrier": individualRecord[10],
                "pricePerPerson": individualRecord[11],
                "priceTotal": individualRecord[12],
                "index": individualRecord[14],
                "flightUrl": individualRecord[15]
            })

            formattedResult = {}
            availableFlightsDictIndex = 0
            flightGroup = []

        
            for i in range(0, len(result)):

                if i % 2 == 0:
                    flightGroup.append(result[i])

                    if (len(flightGroup) > 1):
                        formattedResult[availableFlightsDictIndex] = flightGroup
                        flightGroup = []
                        availableFlightsDictIndex += 1
                else:
                    flightGroup.append(result[i])

                    if (len(flightGroup) > 1):
                        formattedResult[availableFlightsDictIndex] = flightGroup
                        flightGroup = []
                        availableFlightsDictIndex += 1

                


            

            return formattedResult

        else:
            return []
    
    else:
        return []

