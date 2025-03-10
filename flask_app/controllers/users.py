# User routing will go here, home, account, etc...
from dateutil.utils import today
from flask import Flask, render_template
from flask_app import app
import requests
import os
from datetime import date

# Get today's date
raw_today = date.today()

TODAY = raw_today.strftime("%Y/%m/%d")

# Sports API KEY
API_KEY = os.environ.get('NEWS_API')
SPORTS_API = os.environ.get('SPORTS_API')

# Endpoints
NEWS_BASE_URL = "https://newsapi.org/v2/top-headlines"
MLB_URL = f"https://api.sportradar.com/mlb/trial/v8/en/games/{TODAY}/boxscore.json?api_key={SPORTS_API}"


# Parameters for the news request
news_params = {
    "sources": "espn, bleacher-report, sports-illustrated",         # ESPN source ID
    "apiKey": API_KEY,        # API key
    "pageSize": 2,
}

# MLB Scores params
mlb_headers = {"accept": "application/json"}

mlb_response = requests.get(MLB_URL, headers=mlb_headers)
mlb_data = mlb_response.json()

# Created empty list to create into a dictionary list to pass into jinja
cleaned_games = []

# Only gathering 5 games to fit the screen
for game in mlb_data["league"]["games"]:
    game_data = game["game"]
    cleaned_game = {
        "away_team": game_data["away"]["name"],
        "home_team": game_data["home"]["name"],
        "away_runs": game_data["away"]["runs"],
        "home_runs": game_data["home"]["runs"],
        "is_final": game_data["status"] == "closed"  # True if closed, False otherwise
    }
    cleaned_games.append(cleaned_game)

mlb_games = {"games": cleaned_games}


# Making the GET request for news
news_response = requests.get(NEWS_BASE_URL, params=news_params)
news_data = news_response.json()


@app.route('/')
def home():
    return render_template('index.html', article1=news_data['articles'][0], article2=news_data['articles'][1],
                           mlb=mlb_games)


@app.route('/sign-up')
def signup():
    # Sign up will go here
    return render_template('signup.html')


@app.route('/login')
def login():
    # Login will go here
    return render_template('login.html')


@app.route('/nfl')
def nfl():
    return render_template('nfl.html', mlb=mlb_games)