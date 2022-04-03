from asyncio.log import logger
import unittest
from unittest import mock
from unittest.mock import patch
from flask import jsonify
import requests
import os
from main import app, jwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
import logging

 # Use http://127.0.0.1:5000/api/v1 for running locally
baseUrl = "https://group-activity-planning-flask.herokuapp.com/api/v1"

class ApiTest(unittest.TestCase):
   
    def mock_jwt_required(realm):
        return

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        logging.getLogger().setLevel(logging.DEBUG)

    def tearDown(self):
        self.app_context.pop()

    def test1_login_no_credentials(self):
        url = "{}/login".format(baseUrl)
        r = requests.post(url)
        self.assertEqual(r.status_code, 400)

    def test2_login_invalid_credentials(self):
        url = "{}/login".format(baseUrl)
        r = requests.post(url, json={'username': 'wrongemail@gmail.com', 'password': 'WrongPassword'})
        self.assertEqual(r.status_code, 401)
    
    def test3_login_valid_credentials(self):
        url = "{}/login".format(baseUrl)
        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")
        ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD")
        r = requests.post(url, json={'username': ACCESS_USERNAME, 'password': ACCESS_PASSWORD})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
    

  
  
    def test4_refresh_jwt_valid_token(self):
        url = "{}/refresh".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")
        refresh_token = create_refresh_token(identity=ACCESS_USERNAME)

        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }

        r = requests.post(url, headers=headers)
        self.assertEqual(r.status_code, 200)
    

    def test5_refresh_invalid_jwt_type_token(self):
        refreshUrl = "{}/refresh".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")
        refresh_token = create_access_token(identity=ACCESS_USERNAME, fresh=True)

        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }

        r = requests.post(refreshUrl, headers=headers)
        self.assertEqual(r.status_code, 422)

    
    def test7_get_accommodation_error_no_query_params(self):
        accommodationUrl = "{}/accommodation".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")

        access_token = create_access_token(identity=ACCESS_USERNAME, fresh=True)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        r = requests.get(accommodationUrl, headers=headers)
        self.assertEqual(r.status_code, 400)

    
    def test8_get_accommodation_error_no_JWT(self):
        accommodationUrl = "{}/accommodation".format(baseUrl)

        r = requests.get(accommodationUrl)
        self.assertEqual(r.status_code, 401)

    

    def test9_get_accommodation_with_valid_request(self):
        accommodationUrl = "{}/accommodation".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")

        access_token = create_access_token(identity=ACCESS_USERNAME, fresh=True)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            'destinationCity': 'Cork',
            'startDate': '2022-05-14',
            'endDate': '2022-05-16',
            'numberOfPeople': '2',
            'numberOfRooms': '1',
        }

        r = requests.get(accommodationUrl, headers=headers, params=params)
        self.assertEqual(r.status_code, 200)
    

    def test10_get_flights_error_no_JWT(self):
        flightsUrl = "{}/flights".format(baseUrl)

        r = requests.get(flightsUrl)
        self.assertEqual(r.status_code, 401)
    

    def test11_get_flights_error_no_query_params(self):
        flightsUrl = "{}/flights".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")

        access_token = create_access_token(identity=ACCESS_USERNAME, fresh=True)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        r = requests.get(flightsUrl, headers=headers)
        self.assertEqual(r.status_code, 400)
    

    def test12_get_flights_with_valid_request(self):
        flightsUrl = "{}/flights".format(baseUrl)

        ACCESS_USERNAME = os.getenv("ACCESS_USERNAME")

        access_token = create_access_token(identity=ACCESS_USERNAME, fresh=True)

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        params = {
            'fromCity': 'Cork',
            'destinationCity': 'London',
            'startDate': '2022-05-14',
            'endDate': '2022-05-16',
            'numberOfPeople': '2',
        }

        r = requests.get(flightsUrl, headers=headers, params=params)
        self.assertEqual(r.status_code, 200)
if __name__ == '__main__':
    unittest.main()