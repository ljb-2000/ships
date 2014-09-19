from flask import render_template, session, redirect, url_for, current_app, jsonify
from .. import db, admin
from ..models import User, ShipType, Role, Ship, ship_list
from ..email import send_email
from . import main
from .forms import Login
from ..user.forms import Login as LoginForm
from ..user.forms import Register as RegisterForm
from flask.ext.user import current_user, login_required, roles_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask.ext.admin.contrib.sqla import ModelView
import collections

class UserView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_roles('Admin')

    column_list = ('active', 'email', 'handle', 'rsi_profile', 'tas_profile', 'role', 'created_on', 'last_seen')
    column_exclude_list = ('password', 'reset_password_token')
    column_searchable_list = ('email', 'handle')
    form_excluded_columns = ('password', 'reset_password_token', 'avatar_hash', 'created_on', 'last_login')

class RoleView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_roles('Admin')

class ShipView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_roles('Admin')

class ShipTypeView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated(): return False
        return current_user.has_roles('Admin')

    column_labels = dict(name="Ship Type", cnt='Count')
    column_list = ('name', 'cnt', 'image', 'manufacture', 'link')
    column_exclude_list = ('ship_name')
    form_excluded_columns = ('ship_name', 'cnt')

admin.add_view(UserView(User, db.session, endpoint='users'))
admin.add_view(RoleView(Role, db.session, endpoint='roles'))
#admin.add_view(ShipView(Ship, db.session, category='Data', endpoint='ships'))
admin.add_view(ShipTypeView(ShipType, db.session, endpoint='ship-type'))

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

def ship_count():
    ships = Ship.query.all()
    for x in type:
        x.name
    pass

@main.route('/', methods=['GET', 'POST'])
def index():
    ship = ShipType.query.all()
    ship_list = {}
    data = {}
    for x in ship:
        if x.cnt != "0":
            ship_list[x.name]=x.cnt
    data = convert(ship_list)
    return render_template("main/index.html", data=data)