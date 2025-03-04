# User routing will go here, home, account, etc...

from flask import Flask, render_template
from flask_app import app


@app.route('/')
def home():
    return render_template('index.html')