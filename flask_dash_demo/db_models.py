import bcrypt
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def set_password(self, plain_password):
        self.password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))


class Wine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    alcohol = db.Column(db.Float)
    malic_acid = db.Column(db.Float)
    ash = db.Column(db.Float)
    alcalinity_of_ash = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    total_phenols = db.Column(db.Float)
    flavanoids = db.Column(db.Float)
    nonflavanoid_phenols = db.Column(db.Float)
    proanthocyanins = db.Column(db.Float)
    color_intensity = db.Column(db.Float)
    hue = db.Column(db.Float)
    protein = db.Column(db.Float)
    proline = db.Column(db.Float)
    target = db.Column(db.Integer)

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'alcohol': self.alcohol,
            'malic_acid': self.malic_acid,
            'ash': self.ash,
            'alcalinity_of_ash': self.alcalinity_of_ash,
            'magnesium': self.magnesium,
            'total_phenols': self.total_phenols,
            'flavanoids': self.flavanoids,
            'nonflavanoid_phenols': self.nonflavanoid_phenols,
            'proanthocyanins': self.proanthocyanins,
            'color_intensity': self.color_intensity,
            'hue': self.hue,
            'protein': self.protein,
            'proline': self.proline,
            'target': self.target
        }

