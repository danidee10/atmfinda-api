# atmfinda

[![Build Status](https://travis-ci.org/danidee10/atmfinda-api.svg?branch=master)](https://travis-ci.org/danidee10/atmfinda-api)

[![Maintainability](https://api.codeclimate.com/v1/badges/e8ee5d90629fdfbff28f/maintainability)](https://codeclimate.com/github/danidee10/atmfinda-api/maintainability)

API for the atmfinda app

### Installation
```bash
pip install -r requirements.txt
```
Create the Postgres database and enable the postgis extension, the default database in the config file is `atmfinda`, create it and then connect with `psql`

```bash
psql -c atmfinda

# CREATE EXTENSION postgis;
```

### Run the application
Make sure you're in the same directory as `app.py`
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1

flask run
```

### Running the tests
Make sure you're in the same directory where `tests.py` is located i.e The Root directory
```bash
python tests.py
```
