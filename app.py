"""Main app."""

from os import environ
import importlib

import click
from flask import Flask

from .models import db
from .admin import admin


app = Flask(__name__)
app.config.from_object(
    environ.get('FLASK_CONFIG', 'atmfinda.config.config.Local')
)
db.init_app(app)
admin.init_app(app)


# Flask cli scripts
@app.cli.command()
def initdb():
    """Initialize the db."""
    click.echo('initializing')
    db.create_all()
    click.echo('done.')
# End cli scripts


@app.route('/')
def home():
    """Home route."""
    return 'hello world'
