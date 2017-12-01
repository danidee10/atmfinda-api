"""Main app."""

import importlib
from os import environ

import click
import requests

from flask import Flask, jsonify

from sqlalchemy import cast, func
from flask_migrate import Migrate

from .admin import admin
from .models import db, ATM
from .utils import (
    fetch_atms_from_google, transform_google_results, create_atms,
    deserialize_atms
)


app = Flask(__name__)
app.config.from_object(
    environ.get('FLASK_CONFIG', 'atmfinda.config.local')
)
db.init_app(app)
admin.init_app(app)

migrate = Migrate(app, db)


# Flask cli scripts
def initdb():
    """Initialize the db."""
    click.echo('initializing')
    db.create_all()
    click.echo('done.')


@app.cli.command('initdb')
def initdb_command():
    initdb()
# End cli scripts


@app.route('/find-atms-by-coords/<coords>')
def fetch_atms_by_coords(coords):
    """Fetch ATM's by coordinates from Google maps."""
    latitude, longitude = coords.split(',')

    point = 'POINT({} {})'.format(latitude, longitude)

    atms = db.session.query(ATM).filter(
        func.ST_DWithin(ATM.location, point, 5000)
    ).all()

    if atms:
        atms = deserialize_atms(atms)
    else:
        pass
        # Fetch ATM's from google maps and add them to our database
        atms = fetch_atms_from_google(latitude, longitude)
        atms = transform_google_results(atms)

        # Should be done in the background, so we respond as fast as possible
        create_atms(atms)
    
    return jsonify(atms)
