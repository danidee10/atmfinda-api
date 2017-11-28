"""Flask admin.py file."""

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .models import db, ATM

admin = Admin(name='atmfinda', template_mode='bootstrap3')

admin.add_view(ModelView(ATM, db.session))
