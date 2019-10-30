from db_models import User, Wine, db
import json


def create_dummy_user():
    user = User(email='test@test.net', name='Test User', password='foo')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()


def load_wine_data():
    wines = json.load(open('wine.json', 'r'))
    for wine_dict in wines:
        wine = Wine(**wine_dict)
        db.session.add(wine)
    db.session.commit()
