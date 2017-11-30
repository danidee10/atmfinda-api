"""Local Configuration file."""


class Local(object):
    """Local configuration class."""

    DEBUG = True
    SECRET_KEY = 'mysecretkey'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/atmfinda'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    GOOGLE_MAPS_KEY = 'AIzaSyDEb7V54wKCwcCL29K8ZeAZRzk57xRzoDA'


class Production(Local):
    """Production related settings."""
    pass
