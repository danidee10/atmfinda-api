"""Test Settings for Travis CI."""

DEBUG = True
SECRET_KEY = 'mysecretkey'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@postgres/atmfinda'
SQLALCHEMY_TRACK_MODIFICATIONS = True

GOOGLE_MAPS_KEY = ''

DROP_EXISTING_DATABASE = False
