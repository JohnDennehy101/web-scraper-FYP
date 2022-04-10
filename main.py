from dotenv import load_dotenv
import os
import time
from pprint import pprint
from random import randint
from time import sleep
from scrapeAccommodationInfo import extractNumberOfAvailableProperties, stripWhiteSpace, findElementsBeautifulSoup, scrapeHotelInformation, returnScrapedHotelInformation
from scrapeFlightInfo import scrapeFlightInformation
from database import checkDbForExistingRecords
from utils import makeWebScrapeRequest, returnDateComponents, validateDateQueryParameter, validateNumberQueryParameter
from flask import Flask, make_response, render_template, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from datetime import timedelta
from string import Template
from database import insertAccommodationInfo, checkDbForExistingRecords, checkDbForExistingFlightRecords, insertFlightInfo, bootstrapDbOnInitialLoad
from enums import KayakCityCodes, BookingCityDestinationCodes

app = Flask(__name__)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD")

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

@app.before_first_request
def setup():
     bootstrapDbOnInitialLoad()

@app.route("/api/v1/login", methods=["POST"])
def login():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
    
    except:
        return jsonify({"msg": "Must provide username and password"}), 400

    if username != ACCESS_USERNAME or password != ACCESS_PASSWORD:
        # Correct credentials were not provided
        return jsonify({"msg": "Wrong username or password"}), 401
    
    # create a new token with the username stored inside
    access_token = create_access_token(identity=username, fresh=True)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token,refresh_token=refresh_token)

@app.route("/api/v1/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token= create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@app.route('/api/v1/accommodation', methods=['GET'])
@jwt_required(fresh=True)
def create_accommodation_information():
    destinationCity = request.args.get('destinationCity')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    numberOfPeople = request.args.get('numberOfPeople')
    numberOfRooms = request.args.get('numberOfRooms')

    try:
        cityDestinationId = BookingCityDestinationCodes[destinationCity]
    except:
        return jsonify({"msg": "Must provide valid Irish city value for destination city"}), 400

    if not isinstance(destinationCity, str) or not validateDateQueryParameter(startDate) or not validateDateQueryParameter(endDate) or not validateNumberQueryParameter(numberOfPeople) or not validateNumberQueryParameter(numberOfRooms):
        return jsonify({"msg": "Must provide valid values for each query parameter"}), 400

    startDateDict = returnDateComponents(startDate)
    endDateDict = returnDateComponents(endDate)

    existingScrapedRecords = checkDbForExistingRecords(destinationCity, startDate, endDate)

    if existingScrapedRecords:

        if len(existingScrapedRecords) > 0:
            return make_response(jsonify(existingScrapedRecords), 200)

    finalHotelDict = {"resultPages": {
    }}

    hotelSiteUrl = Template("https://www.booking.com/searchresults.en-gb.html?aid=304142&sb_price_type%3Dtotal%3Bsrpvid%3Dff4c997b5ad30070%26%3B=&ss=$destinationCity&is_ski_area=0&ssne=$destinationCity&ssne_untouched=$destinationCity&dest_id=$destinationId&dest_type=city&checkin_year=$checkinYear&checkin_month=$checkinMonth&checkin_monthday=$checkinMonthDay&checkout_year=$checkoutYear&checkout_month=$checkoutMonth&checkout_monthday=$checkoutMonthDay&group_adults=$numberOfPeople&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1")

    finalUrl = hotelSiteUrl.substitute(destinationCity=destinationCity, destinationId=cityDestinationId, checkinYear=startDateDict['year'], checkinMonth=startDateDict['month'], checkinMonthDay=startDateDict['day'], checkoutYear=endDateDict['year'], checkoutMonth=endDateDict['month'], checkoutMonthDay=endDateDict['day'], numberOfPeople=numberOfPeople)

    pageIndex = 1
    hotelHtml = makeWebScrapeRequest(finalUrl)

    hotelResultDict = scrapeHotelInformation(hotelHtml) 
    insertAccommodationInfo(hotelResultDict['propertiesResult'], pageIndex, startDate, endDate)
    finalHotelDict["resultPages"][pageIndex] = hotelResultDict['propertiesResult']
    extractNumberOfAvailableProperties(hotelResultDict['numberOfPropertiesString'])
    
    response = make_response(jsonify(finalHotelDict), 200)
    response.headers["Content-Type"] = "application/json"
    return response




@app.route('/api/v1/flights', methods=['GET'])
@jwt_required(fresh=True)
def create_flight_information():

    fromCity = request.args.get('fromCity')
    destinationCity = request.args.get('destinationCity')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    numberOfPeople = request.args.get('numberOfPeople')
    try:
        departureCityPrefix = KayakCityCodes[fromCity]
        arrivalCityPrefix = KayakCityCodes[destinationCity]
    except:
        return jsonify({"msg": "Must provide valid values cities"}), 400

    if not isinstance(fromCity, str) or not isinstance(destinationCity, str) or not validateDateQueryParameter(startDate) or not validateDateQueryParameter(endDate) or not validateNumberQueryParameter(numberOfPeople):
        return jsonify({"msg": "Must provide valid values for each query parameter"}), 400

    existingScrapedRecords = checkDbForExistingFlightRecords(fromCity, destinationCity, startDate, endDate)

    if existingScrapedRecords and 1 in existingScrapedRecords:
        return make_response(jsonify(existingScrapedRecords), 200)

    
    flightHtml = None
    flightSiteUrl = Template("https://www.kayak.ie/flights/$departureCityPrefix-$arrivalCityPrefix/$startDate/$endDate/$numberOfPeopleadults?sort=bestflight_a")

    completeFlightUrl = flightSiteUrl.substitute(departureCityPrefix=str(departureCityPrefix), arrivalCityPrefix=str(arrivalCityPrefix), startDate=str(startDate)[0:10], endDate=str(endDate)[0:10],numberOfPeopleadults=str(numberOfPeople) + 'adults')

    flightHtml = makeWebScrapeRequest(completeFlightUrl)

    flightResultDict = scrapeFlightInformation(flightHtml)

    sleep(5)
    flightHtml = makeWebScrapeRequest(completeFlightUrl)
    flightResultDict = scrapeFlightInformation(flightHtml)

    sleep(8)
    flightHtml = makeWebScrapeRequest(completeFlightUrl)
    flightResultDict = scrapeFlightInformation(flightHtml)

    insertFlightInfo(flightResultDict, startDate, endDate, fromCity, destinationCity, completeFlightUrl)
    response = make_response(jsonify(flightResultDict), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/api/v1/docs')
def get_docs():
    return render_template('swaggerui.html')



