"""Reusable functions to avoid polluting app.py"""

import importlib
from os import environ

import requests
from shapely import wkb

from .models import db, ATM

CONFIG = environ.get('FLASK_CONFIG', 'atmfinda.config.local')
CONFIG = importlib.import_module(CONFIG)


def transform_google_results(google_results):
    """Transforms results from google's places API to our format"""
    results = []

    if google_results['status'].lower() == 'ok':
        for atm in google_results['results']:
            
            photo_reference = atm['photos'][0]['photo_reference'] \
                if 'photos' in atm else ''
            data = {
                'name': atm['name'], 'address': atm['vicinity'],
                'photo_reference': photo_reference,
                'location': {
                    'latitude': atm['geometry']['location']['lat'],
                    'longitude': atm['geometry']['location']['lat']
                },
                'status': True
            }

            results.append(data)
        return results

    return {'status': 'NO_ATMS_FOUND'}


def create_atms(atms):
    """Takes a list of ATM's in JSON format and saves them to the db."""
    atm_objs = []

    for atm in atms:
        location = atm['location']
        point = 'POINT({} {})'.format(
            location['longitude'], location['latitude']
        )
        del atm['location']

        atm_obj = ATM(**atm, location=point)
        atm_objs.append(atm_obj)

    db.session.add_all(atm_objs)
    db.session.commit()


def fetch_atms_from_google(latitude, longitude):
    """Fetch ATM's from google."""
    url = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
           'location={},{}&radius=5000&type=atm&key={}'.format(
               latitude, longitude, CONFIG.GOOGLE_MAPS_KEY
            )
    )
    response = requests.get(url)

    return response.json()


def deserialize_atms(atms):
    """Takes a list of ATM objects and deserializes them to our format."""
    results = []

    for atm in atms:
        location = wkb.loads(bytes(atm.location.data))

        data = {
            'name': atm.name, 'address': atm.address,
            'photo': atm.photo, 'photo_reference': atm.photo_reference,
            'location': {
                'latitude': location.y, 'longitude': location.x
            },
            'status': atm.status
        }
        results.append(data)

    return results
