# User routing will go here, home, account, etc...
from flask import Flask, render_template
from flask_app import app
import requests
import os

API_KEY = os.environ.get('NEWS_API')

BASE_URL = "https://newsapi.org/v2/top-headlines"

# Parameters for the request
params = {
    "sources": "espn, bleacher-report, sports-illustrated",         # ESPN source ID
    "apiKey": API_KEY,        # API key
    "pageSize": 2,
}

# Make the GET request
response = requests.get(BASE_URL, params=params)
data = response.json()
print(data)


@app.route('/')
def home():
    return render_template('index.html', article1=data['articles'][0], article2=data['articles'][1])


@app.route('/sign-up')
def signup():
    # Sign up will go here
    return render_template('signup.html')


@app.route('/login')
def login():
    # Login will go here
    return render_template('login.html')