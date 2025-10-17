import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

def create_App():

    app = Flask(__name__) 

    import os

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-default-key')


     # Make sure the instance folder exists
    instance_path = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    # Use absolute path for SQLite
    db_path = os.path.join(instance_path, 'expense.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'


    bcrypt = Bcrypt(app)

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    from routes import register_routes
    register_routes(db,app,bcrypt)



    # with app.app_context(): 
    #     db.create_all()

    return app

