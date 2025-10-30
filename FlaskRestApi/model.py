
from datetime import datetime
from app import db

class User(db.Model):  
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable = False)
    notes = db.relationship('Note', backref='owner', lazy=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

