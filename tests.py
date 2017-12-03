"""Test Suite that runs all tests in the 'tests' folder."""

import unittest
import importlib
from os import environ

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from atmfinda.app import app, initdb
from atmfinda.tests import api_tests, utils_tests

CONFIG = environ.get('FLASK_CONFIG', 'atmfinda.config.local_test')
CONFIG = importlib.import_module(CONFIG)


def create_drop_database():
    """Creates/ drop (depending on the CONFIG) the test database."""
    engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI)

    if database_exists(engine.url) and CONFIG.DROP_EXISTING_DATABASE:
        print('Preparing to drop existing database...')
        drop_database(engine.url)

    print('Creating Database...')
    create_database(engine.url)
    print('Finished creating Database.')

    return engine


def enable_postgis(engine):
    """Enable the postgis extensions."""
    print('Enabling postgis extension(s)...')
    conn = engine.connect()
    conn.execute(
        'CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;'
        'CREATE EXTENSION fuzzystrmatch;'
        'CREATE EXTENSION postgis_tiger_geocoder;'
    )
    conn.close()
    print('Finished enabling postgis extensions, Database is ready.')


def destroy_database():
    print('Dropping Database...')
    with app.app_context():
        drop_database(CONFIG.SQLALCHEMY_DATABASE_URI)
    print('Dropped Database.')


def suite():
    """Setup the suite and add tests."""

    engine = create_drop_database()
    enable_postgis(engine)

    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.SQLALCHEMY_DATABASE_URI
    app.testing = True

    with app.app_context():
        initdb()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Patch the TestCases with the app Object
    api_test = api_tests.APITestCase
    api_test.app = app
    utils_test = utils_tests.UtilsTestCase
    utils_test.app = app

    suite.addTests(loader.loadTestsFromTestCase(api_test))
    suite.addTests(loader.loadTestsFromTestCase(utils_test))

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite())

    destroy_database()
