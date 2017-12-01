"""Flask admin.py file."""

from flask_admin import Admin
from flask_admin.contrib.geoa import ModelView

from .models import db, ATM, User

admin = Admin(name='atmfinda', template_mode='bootstrap3')

admin.add_view(ModelView(ATM, db.session))
admin.add_view(ModelView(User, db.session))
