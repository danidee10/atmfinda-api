"""Main app."""

import importlib
from os import environ

import click
import requests

from flask import Flask, jsonify

from sqlalchemy import cast, func
from flask_migrate import Migrate

from .models import db, ATM
from .admin import admin
from .config.config import Local as config


app = Flask(__name__)
app.config.from_object(
    environ.get('FLASK_CONFIG', 'atmfinda.config.config.Local')
)
db.init_app(app)
admin.init_app(app)

migrate = Migrate(app, db)


# Flask cli scripts
@app.cli.command()
def initdb():
    """Initialize the db."""
    click.echo('initializing')
    db.create_all()
    click.echo('done.')
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
        pass
        # wkb.loads(bytes(atms[0].location.data))
    else:
        pass
        # Fetch ATM's from google maps and add them to our database
    
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius=5000&type=atm&key={}'.format(latitude, longitude, config.GOOGLE_MAPS_KEY)
        db.session.add(atm)
        db.session.commit()
        atm = ATM(location='POINT({} {})')
    
    return 'hello world'
