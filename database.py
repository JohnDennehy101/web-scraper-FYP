from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import os

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


def executeListQuery(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


createAccommodationTable = """
CREATE TABLE accommodation (
  accommodationId int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (accommodationId),
  title VARCHAR(60) NOT NULL,
  bookingPreviewLink VARCHAR(700),
  bookingSiteDisplayLocationMapLink VARCHAR(700),
  bookingSiteLink VARCHAR(700),
  freeCancellationText VARCHAR(200),
  locationDistance VARCHAR(100),
  locationTitle VARCHAR(100),
  numberOfBedsRecommendedBooking VARCHAR(100),
  numberOfNightsAndGuests VARCHAR(100),
  numberOfRoomsRecommendedBooking VARCHAR(100),
  price VARCHAR(50),
  ratingScore VARCHAR(50),
  ratingScoreCategory VARCHAR(50),
  reviewQuantity VARCHAR(50),
  roomTypeRecommendedBooking VARCHAR(50),
  pollOptionId VARCHAR(40) NOT NULL,
  page VARCHAR(5),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

insertAccommodationQuery = """
    INSERT INTO accommodation (title, bookingPreviewLink, bookingSiteDisplayLocationMapLink, bookingSiteLink, freeCancellationText, locationDistance, locationTitle, numberOfBedsRecommendedBooking, numberOfNightsAndGuests, numberOfRoomsRecommendedBooking, price, ratingScore, ratingScoreCategory, reviewQuantity, roomTypeRecommendedBooking, pollOptionId, page) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

scrapedValues = [
    ("LYNTOM HOUSE B&B", "https://www.booking.com/hotel/ie/lyntom-house-b-amp-b.en-gb.html?aid=304142&ucfs=1&arphpl=1&checkin=2022-04-06&checkout=2022-04-08&dest_id=-1504189&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=22&hapos=22&sr_order=popularity&srpvid=3c92710f35e8001c&srepoch=1639757088&all_sr_blocks=539150003_204767728_2_1_0&highlighted_blocks=539150003_204767728_2_1_0&matching_block_id=539150003_204767728_2_1_0&sr_pri_blocks=539150003_204767728_2_1_0__16000&from=searchresults#hotelTmpl", "https://www.booking.com/hotel/ie/lyntom-house-b-amp-b.en-gb.html?aid=304142&ucfs=1&arphpl=1&checkin=2022-04-06&checkout=2022-04-08&dest_id=-1504189&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=22&hapos=22&sr_order=popularity&srpvid=3c92710f35e8001c&srepoch=1639757088&all_sr_blocks=539150003_204767728_2_1_0&highlighted_blocks=539150003_204767728_2_1_0&matching_block_id=539150003_204767728_2_1_0&sr_pri_blocks=539150003_204767728_2_1_0__16000&from=searchresults&map=1", "https://www.booking.com/hotel/ie/lyntom-house-b-amp-b.en-gb.html?aid=304142&ucfs=1&arphpl=1&checkin=2022-04-06&checkout=2022-04-08&dest_id=-1504189&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=22&hapos=22&sr_order=popularity&srpvid=3c92710f35e8001c&srepoch=1639757088&all_sr_blocks=539150003_204767728_2_1_0&highlighted_blocks=539150003_204767728_2_1_0&matching_block_id=539150003_204767728_2_1_0&sr_pri_blocks=539150003_204767728_2_1_0__16000&from=searchresults#hotelTmpl", "FREE cancellation", "47.1 km from centre", "Limerick", "2 beds (1 single, 1 double)", "2 nights, 2 adults", "Classic Triple Room", "€ 160", "9.6", "Exceptional", "52 Reviews", "Classic Triple Room", "1234", "1")
]



connection = createDbConnection(DB_HOSTNAME, DB_USERNAME, DB_PASSWORD, DB_NAME)
executeQuery(connection, createAccommodationTable)
executeListQuery(connection, insertAccommodationQuery, scrapedValues)
print(connection)

createDatabaseQuery = "CREATE DATABASE web_scraped_information"

#createDb(connection, createDatabaseQuery)