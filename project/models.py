from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.surname}', '{self.first_name}', '{self.second_name}', '{self.email}', '{self.gender}', '{self.role}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(10), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    booking_hours = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.username}', '{self.email}', '{self.telephone}', '{self.property_type}', '{self.booking_hours}', '{self.date}')"
