from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime

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

    #@property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.username,
           'email': self.email
       }

class Coins(db.Model):
    __tablename__ = 'coins' 
    name  = db.Column(db.String(30))
    symbol  = db.Column(db.String(10), primary_key=True)
    
    def __init__(self, name, symbol):
        self.name  = name
        self.symbol  = symbol

    def __repr__(self):
        return '<Currency: %r, %r >' % (self.name, self.symbol)
 

class Rating(db.Model):
    __tablename__ = 'rating'
    _db = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer )
    symbol_coin  = db.Column(db.String(10), db.ForeignKey('coins.symbol'))
    name_coin = db.relationship('Coins',
        backref=db.backref('rating', lazy='dynamic'))
    market_cap  = db.Column(db.Float)
    price = db.Column(db.Float)
    supply = db.Column(db.Float)
    volume = db.Column(db.Float)
    h1 = db.Column(db.Float)
    h24 = db.Column(db.Float)
    d7 = db.Column(db.Float)
    pub_date = db.Column(db.DateTime)

    def __init__(self, rating, name_coin,  market_cap, price, supply, volume, h1, h24, d7, _date=None):
        self.rating = rating
        self.name_coin  = name_coin
        self.market_cap  = market_cap
        self.price = price
        self.supply = supply
        self.volume = volume
        self.h1 = h1
        self.h24 = h24
        self.d7 = d7
        if _date is None:
            self.pub_date = datetime.utcnow()
        else:
            self.pub_date = _date

    def __repr__(self):
        return '%r, %r, %r, %r' % (self.rating, self.symbol_coin, self.price,  self.pub_date.strftime('%Y-%m-%d %H:%M'))
          

    
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
            'rating': self.rating,
            'symbol_coin': self.symbol_coin,
            'name': self.name_coin.name,
            'market_cap': self.market_cap,
            'price': self.price,
            'supply': self.supply,
            'volume': self.volume,
            'h1': self.h1,
            'h24': self.h24,
            'd7': self.d7,
            'modified_at': self.pub_date.strftime('%Y-%m-%d %H:%M')
       }