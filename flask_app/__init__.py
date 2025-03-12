from flask import Flask
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('DATA_SECRET_KEY')
bcrypt = Bcrypt(app)