# __init__.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)

app.config["MONGO_URI"]='mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/webinar-website'

mongo = PyMongo(app)

cors = CORS(app)

from app import routes