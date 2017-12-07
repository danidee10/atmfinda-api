"""Flask admin.py file."""

from os import environ
from flask_admin import Admin
from flask_admin.contrib.geoa import ModelView

from .models import db, ATM, User

admin = Admin(
    name='atmfinda', url=environ.get('ADMIN_URL', '/admin'),
    template_mode='bootstrap3'
)

admin.add_view(ModelView(ATM, db.session))
admin.add_view(ModelView(User, db.session))
