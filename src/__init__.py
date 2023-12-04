# src/__init__.py
import os  # new-part3
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy  # new-part3



# instantiate the app
app = Flask (__name__)

api = Api (app)

# set config
app.config.from_object('src.config.DevelopmentConfig')  # new
app_settings = os.getenv('APP_SETTINGS')  # new
app.config.from_object(app_settings)      # new

# instantiate the db
db = SQLAlchemy(app)  # new-part3

# model-new class for part -3
class User(db.Model):  # new-part3
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class Ping(Resource):
    def get(self):
        return {
            'status':'success',
            'message':'pong!'
        }
api.add_resource(Ping,'/ping')




