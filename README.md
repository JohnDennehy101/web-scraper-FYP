# Group Activity Planning - Web Scraping Flask API

Name: John Dennehy (20091408)

## Overview.

A Flask API that scrapes Booking.com for accommodation information and Kayak.com for flight information. Scraped results are stored in a SQL database. Requests package used to make external requests to fetch the site html and Beautiful Soup package used to parse the returned html to extract the relevant information. Flask_jwt_extended library used to implement JWT authentication on API routes.

## Live API Url

The API is deployed at the following URL: https://group-activity-planning-flask.herokuapp.com

## Swagger Documentation

Can be found at https://group-activity-planning-flask.herokuapp.com/api/v1/docs

## Setup requirements.

- Open the command line
- Enter the following command in the terminal -
  `git clone https://github.com/JohnDennehy101/web-scraper-FYP`
- Locate the the downloaded folder in the terminal and enter using the following command -
  `cd web-scraper-FYP`
- It's good practice to use a virtual environment before installing the project requirements. Use the following command in the terminal to create a virtual environment - `python3 -m venv env`
- To activate the virtual environment, use the following command - `source env/bin/activate`
- Now project dependencies need to be installed, enter the following command in the terminal - `pip install -r requirements.txt`
- To get the app functional, a .env file needs to be added to the project. To do this, enter the following command - `touch .env`
- The .env file should now be created. To edit this file, enter the following - `nano .env`
- A nano editor should now be displayed in terminal with the .env file open. This now needs to be populated with the relevant environment variables list below.

  - JWT_SECRET_KEY={populate this with a password of your choice}
  - ACCESS_USERNAME={Enter a private username that you will use for authorization}
  - ACCESS_PASSWORD={Enter a private password that you will use for authorization}
  - DB_PASSWORD={Enter the password of your local postgres db here}
  - DB_HOSTNAME=localhost
  - DB_USERNAME=root
  - DB_NAME={name of db that you want to use locally}

- Save the .env file `(Ctrl + O)`
- To exit the file enter `(Ctrl + X)`
- You need to have a Postgres database running locally for the API to function locally.
- Once all this is complete, enter `FLASK_APP=main.py FLASK_ENV=development flask run ` to get the project running locally on localhost.
- You can then navigate to the Swagger documents locally at `http://127.0.0.1:5000/api/v1/docs`
- To stop the Flask server locally, hit CTRL and C in the terminal to kill the process.
