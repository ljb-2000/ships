from flask import abort, flash, render_template, session, redirect, url_for, current_app, jsonify
from .. import db
from ..models import User, ShipType, Role, Ship, ship_list
from . import user
from forms import EditProfile, AddShip
from flask.ext.user import current_user, login_required, roles_required, UserManager, UserMixin, SQLAlchemyAdapter

@user.before_app_request
def before_request():
    if current_user.is_authenticated():
        current_user.seen()

@login_required
@user.route('/user/<handle>/')
def profile(handle):
    user = User.query.filter_by(handle=handle).first()
    if user is None:
        abort(404)

    ships = {}
    list = user.ships_list
    for x in list:
        ship = Ship.query.filter_by(ship_name=x).first()
        sid = ship.ship_type
        type = ShipType.query.filter_by(id=sid).first()
        name = type.name
        ships[x]=name.encode('utf-8')

    return render_template('user/profile.html', user=user, ships=ships)

@login_required
@user.route('/user/edit-profile/', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfile()
    user = User.query.filter_by(email=current_user.email).first()
    if form.validate_on_submit():
        current_user.handle = form.handle.data
        current_user.rsi_profile = form.rsi_profile.data
        current_user.tas_profile = form.tas_profile.data
        current_user.hide_email = form.hide_email.data
        db.session.add(user)
        flash('Your profile has been updated.', 'info')
        return redirect(url_for('user.profile', handle=current_user.handle))
    form.handle.data = current_user.handle
    form.rsi_profile.data = current_user.rsi_profile
    form.tas_profile.data = current_user.tas_profile
    form.hide_email.data = current_user.hide_email
    return render_template('user/edit_profile.html', form=form)

@login_required
@user.route('/user/add-ship/', methods=['GET', 'POST'])
def add_ship():
    form = AddShip()
    if form.validate_on_submit():
        ship_type = form.ship_type.data
        #ship_id = ShipType.query.filter_by(name=ship_type).first()
        shiptype = ship_type.id
        ship = Ship(ship_name=form.ship_name.data,
                    ship_type=shiptype)
        db.session.add(ship)
        flash('Your ship has been added.', 'info')
        if current_user.handle is None:
            return redirect(url_for('main.index'))
        else:
            return redirect(url_for('user.profile', handle=current_user.handle))
    return render_template('user/add_ship.html', form=form)