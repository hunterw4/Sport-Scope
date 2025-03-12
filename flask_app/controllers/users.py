# User routing will go here, home, account, etc...
from dateutil.utils import today
from flask import Flask, render_template, redirect, request, flash, session, make_response
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask_app.models.user import User
import requests
import os
from datetime import date
bcrypt = Bcrypt()

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

# Define Default Data Incase API response is bad to avoid crashing
mlb_data = {
    "league": {
        "games": []
        }
    }

news_data = {
    "articles": [None, None]
    }



# MLB Scores params
mlb_headers = {"accept": "application/json"}

mlb_response = requests.get(MLB_URL, headers=mlb_headers)
if mlb_response.ok:
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
if news_response.ok:
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

@app.route('/nfl/<id>')
def team_roster(id):
    url = f"https://api.sportradar.com/nfl/official/trial/v7/en/teams/{id}/full_roster.json?api_key={SPORTS_API}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    roster_data = response.json()
    
    coaches = roster_data.get('coaches', [])
    players = roster_data.get('players', [])
    if response:
        return render_template('roster.html', mlb=mlb_games, coaches=coaches, players=players)
    else:
        return render_template('roster.html')



#---   User Dash   ---------------------------------------------------
@app.route('/dashboard')
def user_dashboard():
    if 'user_id' in session:
        data = {
            "id" : session['user_id']
        }
        print(data)
        user = User.get_id(data)
        return render_template('user_dashboard.html', user=user)


#---   Picking a favorite team ----------------------------------

@app.route('/favorite_team', methods=['POST'])
def favorite_team_pick():
    if 'user_id' in session:
    
        updated_data = {
            "id" : session['user_id'],
            "favorite_team_id" : request.form["favorite_team_id"],
            "favorite_team_name" : request.form["favorite_team_name"]
        }
        print(updated_data)
        result = User.update_favorite_team(updated_data)
        print(result)

        return redirect('/dashboard')
    else:
        flash("Must log in first","warning" )
        return redirect('/nfl')




# #---   Picking Favorite Player    ----------------------------------

@app.route('/favorite_player', methods=['POST'])
def favorite_player():
    if 'user_id' in session:
        updated_data = {
            "id" : session['user_id'],
            "player_position" : request.form["player_position"],
            "favorite_player" : request.form["player_name"]
        }
        print(updated_data)
        result = User.update_favorite_player(updated_data)
        print(result)

        return redirect('/dashboard')
    else:
        flash("Must log in first","warning" )
        return redirect('/nfl')


    


#---   Registering Account   -----------------------------------------------
@app.route('/register', methods=["GET", "POST"])
def register_account():
    if request.method == 'POST':
        if not User.validate_register(request.form):
            return redirect('/sign-up')
        
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords do not match.", "register_error")
            return redirect('/sign-up')
        
        existing_user = User.get_email({"email": request.form['email']})
        if existing_user:
            flash("Email already exists. Please log in.", "register_error")
            return redirect('/sign-up')
        
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        register_user = {
            "name": request.form["name"],
            "email": request.form["email"],
            "password": pw_hash
        }
        User.save_user(register_user)
        flash("You have been registered! Please log in.", "register_success")
        return redirect('/sign-up')
    
    return render_template('login.html')



#---   Login   ------------------------------------------------------
@app.route('/submit_login', methods=['POST'])
def submit_login():
    if not User.validate_login(request.form):
        print('fail 1')
        return redirect('/login')
    
    user = User.get_email({"email": request.form['email']})
    
    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = user.id
        session['name'] = user.name
        session["email"] = user.email
        flash("Login was successful!", "login_success")
        print('success')
        return redirect('/dashboard')
    
    flash("Your Email/Password combination doesn't match or email not found.", "login_error")
    print('fail 2')
    return redirect('/login')



#---   Logout Of Dashboard   -----------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "logout_info")
    return redirect("/login")


