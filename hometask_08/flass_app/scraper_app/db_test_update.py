from datetime import datetime
from models import User, Coins, Rating, db
import sys
sys.path.insert(0, '../')
from flask_example import app


if __name__ == '__main__':
    with app.app_context() as context:
        db.init_app(context.app)

        coins =[Coins('Coin1', 'C1'),
             Coins('Coin2', 'C2')]
 

        now =  datetime.utcnow()
        rates = [Rating(1, coins[1], 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, now ),
                 Rating(2, coins[1], 1.2, 2.2, 3.2, 4.2, 5.2, 6.2, 7.2, now ),
                 Rating(3, coins[0], 1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, now ),
                Rating(4, coins[0], 1.4, 2.4, 3.4, 4.4, 5.4, 6.4, 7.4, now ) ]

        
        #check if coin exist, otherwise add it
        for c in coins:
            if Coins.query.filter_by(symbol = c.symbol).count() == 0:
                db.session.add(c)

        for rate in rates:
            db.session.add(rate)
         
        
         
            
        db.session.commit()

        #Queries on related fields example'''
        print("Rating" + "*"*20)
        coins = Coins.query.all()
        for c in coins:
            print(c)
            
        print("Rating" + "*"*20)
        rating = Rating.query.all()
        for r in rating:
             #print('rating and coin name by foreign key: {}'.format(r.name_coin.name))
             print('rating: {}'.format(r))
        
        #     a_id = r.symbol_coin
         #    coin = Coins.query.filter_by(symbol = a_id).first()
             #print('Author nickname by Authors model filter with _id field: {}'.format(coin.name))
             
