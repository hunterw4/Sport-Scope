from flask import Flask
from flask_bcrypt import Bcrypt
import os

secret_key = os.environ.get('DATA_SECRET_KEY')

if secret_key:
    app = Flask(__name__)
    app.secret_key = secret_key
    bcrypt = Bcrypt(app)
else:
    print("Enviorment Variable Not Found")