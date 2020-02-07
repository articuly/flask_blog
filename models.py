from libs import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    realname = db.Column(db.String)
    sex = db.Column(db.Integer)
    city = db.Column(db.String)
    hobby = db.Column(db.String)
    intro = db.Column(db.String)

class Article(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    intro=db.Column(db.String)
    author=db.Column(db.String)
    content=db.Column(db.Text)
    pubdate=db.Column(db.DateTime, default=datetime.now)
