"""Local Configuration file."""


class Local(object):
    """Local configuration class."""

    DEBUG = True
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/myapp.db'


class Production(Local):
    """Production related settings."""
    pass
