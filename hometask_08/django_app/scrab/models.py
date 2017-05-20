from django.db import models

from django.utils import timezone
# Create your models here.

class User(models.Model):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128) 
    email = models.TextField()
    pw_hash = models.TextField()


    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.username,
           'email': self.email
       }


class Coins(models.Model):
    name  = models.CharField(max_length=128) 
    symbol  = models.CharField(max_length=10)


    class Meta:
        verbose_name_plural = 'Coins'
        #unique combination of fields
        unique_together = (("name", "symbol"),)
    
    def __repr__(self):
        return '<Currency: %r, %r >' % (self.name, self.symbol)

    def __str__(self):
        return '%r, %r ' % (self.name, self.symbol)
 

class Rating(models.Model):

    _db = models.AutoField(primary_key=True)
    rating = models.IntegerField() 
    name_coin = models.ForeignKey(
        'Coins',
        on_delete=models.CASCADE,
    )
    market_cap  = models.FloatField()
    price = models.FloatField()
    supply = models.FloatField()
    volume = models.FloatField()
    h1 = models.FloatField()
    h24 = models.FloatField()
    d7 = models.FloatField()
    pub_date = models.DateTimeField(default=timezone.now)


    class Meta:
        get_latest_by = 'pub_date'
        ordering = ["-pub_date"]
        
    def __repr__(self):
        return '%r, %r, %r, %r' % (self.rating, self.symbol_coin, self.price,  self.pub_date.strftime('%Y-%m-%d %H:%M'))

    def __str__(self):
        return '%r, %r, %r, %r' % (self.rating, self.name_coin.symbol, self.price,  self.pub_date.strftime('%Y-%m-%d %H:%M'))


    
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
 

