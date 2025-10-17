from app import db 
from datetime import date
from flask_login import UserMixin


class User(db.Model,UserMixin): 

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String ,nullable=False)
    password = db.Column(db.String ,nullable = False)

    expenses = db.relationship('Expense',backref = 'user',lazy=True)
class Expense(db.Model): 

    id = db.Column(db.Integer,primary_key = True)
    description = db.Column(db.String(120),nullable = False)
    category = db.Column(db.String(50),nullable = False)
    amount = db.Column(db.Float,nullable = False)
    date = db.Column(db.Date ,nullable = False,default = date.today)

    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)


