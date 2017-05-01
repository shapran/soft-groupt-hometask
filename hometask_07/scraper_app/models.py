from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def lower(field):
    return func.lower(field)

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    email = db.Column(db.Text)
    pw_hash = db.Column(db.Text)

    def __init__(self, username, email, pw_hash):
        self.username = username
        self.email = email
        self.pw_hash = pw_hash

    def __repr__(self):
        return '<User %r>' % self.username

 
class Overclockers(db.Model):
    __tablename__ = 'Overclockers'
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    author = db.Column(db.Text)
    text = db.Column(db.Text)
    price = db.Column(db.Integer)
    currency = db.Column(db.Text)

    def __init__(self, title, url, author, text, price, currency):
        self.author = author
        self.title = title
        self.url = url
        self.text = text
        self.price = price
        self.currency = currency

    def __repr__(self):
        return '<%r, %r by %r, %r, %r>' % (self.title, self.url, self.author, self.price, self.currency)
 
class Topics(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors._id'))
    author = db.relationship('Authors',
                                 backref=db.backref('topics', lazy='dynamic'))
    title = db.Column(db.Text)
    url = db.Column(db.Text)

    def __init__(self, author, title, url):
        self.author = author
        self.title = title
        self.url = url

    def __repr__(self):
        return '<%r by %r>' % (self.title, self.author)

class Authors(db.Model):

    _id = db.Column(db.Integer, primary_key=True)
    nickname =  db.Column(db.String(128))

    def __init__(self, nickname):
        self.nickname = nickname

    def __repr__(self):
        return '<User nick: %r>' % self.nickname
