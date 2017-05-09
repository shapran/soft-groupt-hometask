from models import User, Coins, Rating, db
import sys
sys.path.insert(0, '../')
from flask_example import app
from datetime import datetime


if __name__ == '__main__':
    with app.app_context() as context:
        db.init_app(context.app)

        #create db
        db.drop_all() 
        db.create_all()

        sys.exit(0)
        '''
        
        coin1 = Coins('Coin1', 'C1')
        coin2 = Coins('Coin2', 'C2')
        coin3 = Coins('Coin3', 'C3')

        now =  datetime.utcnow()
        topic1 = Rating(1, coin1, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 )
        topic2 = Rating(2, coin2, 1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2 )
        topic3 = Rating(3, coin3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3 )
        topic4 = Rating(4, coin2, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4 , now)

        db.session.add(coin1)
        db.session.add(coin2)
        db.session.add(coin3)
        db.session.add(topic1)
        db.session.add(topic2)
        db.session.add(topic3)
        db.session.add(topic4)

        db.session.commit()

        print("Rating" + "*"*20)
        rating = Rating.query.all()
        for r in rating:
             #print('rating and coin name by foreign key: {}'.format(r.name_coin.name))
             print('rating: {}'.format(r))
    

        #Queries on related fields example 
        rating = Rating.query.all()
        for r in rating:
             print('rating and coin name by foreign key: {}'.format(r.name_coin.name))
        
             a_id = r.symbol_coin
             coin = Coins.query.filter_by(symbol = a_id).first()
             print('Author nickname by Authors model filter with _id field: {}'.format(coin.name))
             
'''
