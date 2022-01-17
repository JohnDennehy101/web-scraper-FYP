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


def insertAccommodationInfo(accommodationList, page, startDate, endDate, eventId):
    accommodationInfoForDbInsertion = []
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    for i in range(0, len(accommodationList)):
        individualItem = (startDateString, endDateString, accommodationList[i]["title"], accommodationList[i]["bookingPreviewLink"], accommodationList[i]["bookingSiteDisplayLocationMapLink"], accommodationList[i]["bookingSiteLink"], accommodationList[i]["freeCancellationText"], accommodationList[i]["locationDistance"], accommodationList[i]["locationTitle"], accommodationList[i]["numberOfBedsRecommendedBooking"], accommodationList[i]["numberOfNightsAndGuests"], accommodationList[i]["numberOfRoomsRecommendedBooking"], accommodationList[i]["price"], accommodationList[i]["ratingScore"], accommodationList[i]["ratingScoreCategory"], accommodationList[i]["reviewQuantity"], accommodationList[i]["roomTypeRecommendedBooking"], str(page), eventId)
        accommodationInfoForDbInsertion.append(individualItem)
    

    insertAccommodationQuery = """
    INSERT INTO accommodation (startDate, endDate, title, bookingPreviewLink, bookingSiteDisplayLocationMapLink, bookingSiteLink, freeCancellationText, locationDistance, locationTitle, numberOfBedsRecommendedBooking, numberOfNightsAndGuests, numberOfRoomsRecommendedBooking, price, ratingScore, ratingScoreCategory, reviewQuantity, roomTypeRecommendedBooking, page, eventId) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    executeListQuery(connection, insertAccommodationQuery, accommodationInfoForDbInsertion)
    


def checkDbForExistingRecords(destinationCity, startDate, endDate):
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
    startDateString = returnStringDateRepresentation(startDate)
    endDateString = returnStringDateRepresentation(endDate)

    timestampMinusADay = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    existingRecordsQuery = """
    SELECT * FROM accommodation
    WHERE locationTitle = '{}' AND startDate = '{}' AND endDate = '{}' AND timestamp > '{}'
    """.format(destinationCity, startDateString, endDateString, timestampMinusADay)

    

    dbRecords = readQuery(connection, existingRecordsQuery)

    if len(dbRecords) > 0:

        result = {"resultPages": {
            "1": [],
            "2": [],
            "3": []
    }}


        for record in range(len(dbRecords)):
           
            individualRecord = list(dbRecords[record])
            page = individualRecord[18]

            result["resultPages"][page].append({
             "title": individualRecord[3],
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


def getExistingAccommodationRecords(destinationCity, eventId):
    connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)

    timestampMinusADay = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    existingRecordsQuery = """
    SELECT * FROM accommodation
    WHERE locationTitle LIKE('%{}%') AND eventId = '{}' AND timestamp > '{}'
    """.format(destinationCity, eventId, timestampMinusADay)

    

    dbRecords = readQuery(connection, existingRecordsQuery)

    if len(dbRecords) > 0:

        result = {"resultPages": {
            "1": [],
            "2": [],
            "3": []
    }}


        for record in range(len(dbRecords)):
           
            individualRecord = list(dbRecords[record])
            page = individualRecord[18]

            result["resultPages"][page].append({
             "title": individualRecord[3],
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


createAccommodationTable = """
CREATE TABLE accommodation (
  accommodationId int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (accommodationId),
  startDate VARCHAR (100),
  endDate VARCHAR (100),
  title VARCHAR(60) NOT NULL,
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
  eventId VARCHAR(200),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


"""
connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
executeQuery(connection, createAccommodationTable)
#executeListQuery(connection, insertAccommodationQuery, scrapedValues)
print(connection)

createDatabaseQuery = "CREATE DATABASE web_scraped_information"

#createDb(connection, createDatabaseQuery)
"""
