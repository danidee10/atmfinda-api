"""SQLAlchemy models."""

import importlib
from os import environ

from geoalchemy2 import Geography
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeSerializer
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

CONFIG = environ.get('FLASK_CONFIG', 'atmfinda.config.local')
CONFIG = importlib.import_module(CONFIG)

db = SQLAlchemy()


class Base(db.Model):
    """Base model that implements some basic fields needed in other models."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class ATM(Base):
    """ATM model to store the details of the ATM and the active status."""

    __tablename__ = 'atm'

    name = db.Column(db.String, nullable=False)
    place_id = db.Column(db.String, default='')
    address = db.Column(db.String)
    photo_reference = db.Column(db.String, default='')
    photo = db.Column(db.String, default='')
    location = db.Column(Geography('POINT'), nullable=False)
    status = db.Column(db.Boolean, default=True)


class User(Base):
    """Model for storing User details."""

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    @staticmethod
    def generate_password_hash(password):
        """Generate a salted password hash."""
        return generate_password_hash(password)

    @staticmethod
    def check_password(password, password_hash):
        """Check if the password against a hash."""
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_token(data):
        """Generate a token after a user has been authenticated succesfully."""
        s = URLSafeSerializer(CONFIG.SECRET_KEY)

        return s.dumps(data)

    @classmethod
    def authenticate(cls, email, password):
        """Authenticates a user using their email and password."""
        user = db.session.query(cls).filter_by(email=email).first()

        password_hash = getattr(user, 'password_hash', None)
        
        if user and cls.check_password(password, password_hash):
            return True

        return False


class ATMUpdateLog(Base):
    """Model for storing details about an ATM Update by a user."""

    atm_id = db.Column(db.Integer, db.ForeignKey('atm.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),  nullable=False)

    atm = db.relationship('ATM', backref=db.backref('update_logs', lazy=True))
    user = db.relationship('User', backref=db.backref('users', lazy=True))
