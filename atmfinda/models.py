"""SQLAlchemy models."""

from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography


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

    name = db.Column(db.String, nullable=False)
    place_id = db.Column(db.String, default='')
    address = db.Column(db.String)
    photo_reference = db.Column(db.String, default='')
    photo = db.Column(db.String, default='')
    location = db.Column(Geography('POINT'), nullable=False)
    status = db.Column(db.Boolean, default=True)
