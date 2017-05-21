from flask_example import app
from models import User, Coins, Rating, db
from sqlalchemy import Index, func
import time

with app.app_context() as context:
    db.init_app(context.app)
#     idx = Index('rating_pd_idx', Rating.pub_date)
#     idx.create(db.get_engine())
    start = time.time()
    r = db.session.query(func.max(Rating.pub_date)).with_hint(Rating, 'USE INDEX (rating_pd_idx)')
    ratings = Rating.query.filter_by(pub_date=r)
    # ratings = Rating.query.distinct(Rating.name_coin)
    print([r for r in ratings])
    print(time.time() - start)