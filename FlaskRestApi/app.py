from flask import Flask  
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
import os 
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(): 
    app = Flask(__name__) 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 

    api = Api(app)
    db.init_app(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    from notes import notes_register
    notes_register(app,api,bcrypt,jwt)


    return app,api

