from main import db
from datetime import datetime,timezone 
from flask_login import UserMixin

class User(db.Model,UserMixin): 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String ,nullable = False )
    password = db.Column(db.String)

    tasks = db.relationship('MyTask', backref='owner', lazy=True)


class MyTask(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(100),nullable=False)
    complete= db.Column(db.Integer,default= 0)
    created = db.Column(db.DateTime,default = datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User {self.id}"
