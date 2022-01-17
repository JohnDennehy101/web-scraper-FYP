from dotenv import load_dotenv
import os
import time
from pprint import pprint
from random import randint
from time import sleep
from scrapeAccommodationInfo import extractNumberOfAvailableProperties, stripWhiteSpace, findElementsBeautifulSoup, scrapeHotelInformation, returnScrapedHotelInformation
from scrapeFlightInfo import scrapeFlightInformation
from database import checkDbForExistingRecords
from utils import makeWebScrapeRequest, returnDateComponents
from flask import Flask, make_response, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from datetime import timedelta
from string import Template
from database import insertAccommodationInfo, getExistingAccommodationRecords

app = Flask(__name__)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD")

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if username != ACCESS_USERNAME or password != ACCESS_PASSWORD:
        # Correct credentials were not provided
        return jsonify({"msg": "Wrong username or password"}), 401
    
    # create a new token with the username stored inside
    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token,refresh_token=refresh_token)

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token= create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@app.route('/accommodation', methods=['POST'])
@jwt_required(fresh=True)
def create_accommodation_information():
    data = request.get_json()
    destinationCity = data['destinationCity']
    startDate = data['startDate']
    endDate = data['endDate']
    numberOfPeople = data['numberOfPeople']
    numberOfRooms = data['numberOfRooms']
    eventId = data['eventId']

    startDateDict = returnDateComponents(startDate)
    endDateDict = returnDateComponents(endDate)

    existingScrapedRecords = checkDbForExistingRecords(destinationCity, startDate, endDate)


    if len(existingScrapedRecords) > 0:
        return make_response(jsonify(existingScrapedRecords), 200)

    additionalPage = True
    offset = 0
    offsetQueryParameter = ''
    finalHotelDict = {"resultPages": {
    }}

    while additionalPage:
        #Still need to map destination ids to dict so that they can be dynamically loaded into url
        hotelSiteUrl = Template("https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=$destinationCity&is_ski_area=0&ssne=$destinationCity&ssne_untouched=$destinationCity&dest_id=-1503733&dest_type=city&checkin_year=$checkinYear&checkin_month=$checkinMonth&checkin_monthday=$checkinMonthDay&checkout_year=$checkoutYear&checkout_month=$checkoutMonth&checkout_monthday=$checkoutMonthDay&group_adults=$numberOfPeople&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1")

        hotelSiteUrl.substitute(destinationCity=destinationCity, checkinYear=startDateDict['year'], checkinMonth=startDateDict['month'], checkinMonthDay=startDateDict['day'], checkoutYear=endDateDict['year'], checkoutMonth=endDateDict['month'], checkoutMonthDay=endDateDict['day'], numberOfPeople=numberOfPeople)

        pageIndex = 1
    
        if offset > 0:
            offsetQueryParameter = "&offset={quantity}".format(quantity=offset)
            hotelSiteUrl += offsetQueryParameter
    

        print(hotelSiteUrl.substitute(destinationCity=destinationCity, checkinYear=startDateDict['year'], checkinMonth=startDateDict['month'], checkinMonthDay=startDateDict['day'], checkoutYear=endDateDict['year'], checkoutMonth=endDateDict['month'], checkoutMonthDay=endDateDict['day'], numberOfPeople=numberOfPeople))
        print(offset)
        hotelHtml = None
        #flightHtml = makeWebScrapeRequest(flightSiteUrl)
        #hotelHtml = makeWebScrapeRequest(hotelSiteUrl)
   

    
    
        with open('limerick_booking.com.html', 'r') as f:
            contents = f.read()
            hotelHtml = contents
    
 
        
    
        #sleep(randint(5,15))
        hotelResultDict = scrapeHotelInformation(hotelHtml, offset) 
        insertAccommodationInfo(hotelResultDict['propertiesResult'], pageIndex, startDate, endDate, eventId)
        #finalHotelDict.append(hotelResultDict['propertiesResult'])
        finalHotelDict["resultPages"][pageIndex] = hotelResultDict['propertiesResult']
        numberOfProperties = extractNumberOfAvailableProperties(hotelResultDict['numberOfPropertiesString'])
        pageIndex += 1
        offset += 25
        #if (numberOfProperties - offset) < 0:
        if offset == 50:
            additionalPage = False
        additionalPage = False
    
    with open("results.txt", "w") as file:
        file.write(str(finalHotelDict))
    
    headers = {"Content-Type": "application/json"}
    response = make_response(jsonify(finalHotelDict), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/accommodation', methods=['GET'])
@jwt_required(fresh=True)
def get_accommodation_information():
    destinationCity = request.args.get('destinationCity')
    eventId = request.args.get('eventId')

    existingScrapedRecords = getExistingAccommodationRecords(destinationCity, eventId)
    headers = {"Content-Type": "application/json"}
    response = make_response(jsonify(existingScrapedRecords), 200)
    response.headers["Content-Type"] = "application/json"
    return response




@app.route('/flights', methods=['GET'])
@jwt_required(fresh=True)
def get_flight_information():

    fromCity = request.args.get('fromCity')
    destinationCity = request.args.get('destinationCity')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    numberOfPeople = request.args.get('numberOfPeople')
    """
    flightHtml = makeWebScrapeRequest(flightSiteUrl)
    flightResultDict = scrapeFlightInformation(flightHtml)
    """

    flightHtml = None
    #Still need to map destination ids to dict so that they can be dynamically loaded into url
    flightSiteUrl = Template("https://www.kayak.ie/flights/ORK-PAR/$startDate/$endDate/$numberOfPeopleadults?sort=bestflight_a")

    print(flightSiteUrl.substitute(startDate=str(startDate)[0:10], endDate=str(endDate)[0:10],numberOfPeopleadults=str(numberOfPeople) + 'adults'))

    with open('dublin_london_kayak.com.html', 'r') as f:
        contents = f.read()
        flightHtml = contents
    flightResultDict = scrapeFlightInformation(flightHtml)
    with open("kayak-results.txt", "w") as file:
        file.write(str(flightResultDict))

    response = make_response(jsonify(flightResultDict), 200)
    response.headers["Content-Type"] = "application/json"
    return response



