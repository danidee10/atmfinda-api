"""SQLAlchemy models."""

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry


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

    location = db.Column(Geometry('POINT'))
    status = db.Column(db.Boolean, default=True)
