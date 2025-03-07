# User routing will go here, home, account, etc...

from flask import Flask, render_template
from flask_app import app


@app.route('/')
def home():
    return render_template('index.html')




@app.route('/sign-up')
def signup():
    # Sign up will go here
    return render_template('signup.html')


@app.route('/login')
def login():
    # Login will go here
    return render_template('login.html')