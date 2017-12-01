"""Main app."""

import importlib
from os import environ

import click
import requests

from flask import Flask, Response, request, jsonify, abort

from sqlalchemy import cast, func
from flask_migrate import Migrate

from .admin import admin
from .models import db, ATM, User
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


@app.route('/users/new', methods=['POST'])
def create_new_user():
    """Create a new user."""
    data = request.get_json()

    user = db.session.query(User).filter_by(email=data['email']).first()

    if user:
        return abort(
            403, Response(
                {'message': 'A user with this email already exists'}
            )
        )

    # Generate the hash and save it to the data dict
    password_hash = User.generate_password_hash(data['password'])
    del data['password']
    data['password_hash'] = password_hash

    user = User(**data)
    
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User Created Succesfully'})


@app.route('/users/signin', methods=['POST'])
def sign_user_in():
    """Signs the user in and returns an auth Token."""
    data = request.get_json()
    email = data['email']
    
    if User.authenticate(email, data['password']):
        token = User.generate_token(email)

        return jsonify(
            {'message': 'User Authenticated Succesfully', 'token': token}
        )

    return jsonify({'message': 'Invalid Login Credentials'})

@app.route('/find-atms-by-coords/<coords>')
def fetch_atms_by_coords(coords):
    """Fetch ATM's by coordinates from Google maps."""
    latitude, longitude = coords.split(',')

    point = 'POINT({} {})'.format(longitude, latitude)

    atms = db.session.query(ATM).filter(
        func.ST_DWithin(ATM.location, point, 5000)
    ).all()

    if atms:
        atms = deserialize_atms(atms)
    else:
        # Fetch ATM's from google maps and add them to our database
        atms = fetch_atms_from_google(latitude, longitude)
        atms = transform_google_results(atms)

        # Should be done in the background, so we respond as fast as possible
        create_atms(atms)
    
    return jsonify(atms)
