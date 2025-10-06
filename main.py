# imports 
from flask import Flask,flash,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os





db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-default-key')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db.init_app(app)

    login_manager = LoginManager(app)
    from model import User
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("⚠️ Please login first to continue.", "danger")
        return redirect(url_for('login'))


    bcrypt = Bcrypt(app)

    from routes import app_routes
    app_routes(app,db,bcrypt)

    return app









