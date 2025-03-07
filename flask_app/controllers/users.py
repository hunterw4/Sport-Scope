# User routing will go here, home, account, etc...

from flask import Flask, render_template,redirect,flash,session,request
from flask_app import app
from flask_app.models.user import users
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'passwd':None
    }
    if isValid(data,request.form['passwd']) != True:
        return redirect('/register')
        
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_info =  users.get_user_by_email(data)
    return redirect('/dashboard')