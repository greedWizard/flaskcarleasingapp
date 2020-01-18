from flaskcarleasing.config import db, login_manager
from datetime import datetime
import hashlib
from flask_login import UserMixin

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)
    price_per_day = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, default='description')

    concern_id = db.Column(db.Integer, db.ForeignKey('concern.id'), nullable=False)
    concern = db.relationship('Concern', backref=db.backref('cars', lazy=True, \
        cascade="all, delete-orphan"))

    pic = db.Column(db.String(37), nullable=False, default='default.png')

    def __repr__(self):
        return f'<Car {self.concern.title} {self.model}>'


class Concern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False, unique=True)

    superuser = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username} {self.phone_number} type {self.superuser}>'


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('contracts', lazy=True))

    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = db.relationship('Car', backref=db.backref('contracts', lazy=True))

    lease_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)
    actual_return_date = db.Column(db.DateTime, nullable=True)

    penalty = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    total_price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Contract {self.user} | {self.car}>'