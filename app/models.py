from datetime import datetime
from flask import request
import hashlib
from . import db
from . import UserMixin

ship_list = db.Table('ship_list',
                     db.Column('id', db.Integer(), primary_key=True),
                     db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('ship_id', db.Integer, db.ForeignKey('ship.id')))

user_roles = db.Table('user_roles',
                      db.Column('id', db.Integer(), primary_key=True),
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    password = db.Column(db.String(255), nullable=False, default='')
    handle = db.Column(db.String(64), unique=True, nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    hide_email = db.Column(db.Boolean, default=True)
    avatar_hash = db.Column(db.String(32))
    rsi_profile = db.Column(db.String(255), nullable=True)
    tas_profile = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    roles = db.relationship('Role',
                            secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime,  default=datetime.utcnow)
    ships_list = db.relationship('Ship',
                                 secondary=ship_list,
                                 backref=db.backref('user', lazy='dynamic'),
                                 lazy='dynamic')
    #def __init__(self, **kwargs):
    #    if self.email is not None and self.avatar_hash is None:
    #        self.avatar_hash = hashlib.md5(
    #            self.email.encode('utf-8').hexdigest())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def seen(self):
        self.last_login = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return self.handle

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return self.name

class Ship(db.Model):
    __tablename__ = 'ship'
    id = db.Column(db.Integer, primary_key=True)
    ship_type = db.Column(db.Integer, db.ForeignKey('shiptype.id'))
    ship_name = db.Column(db.String(255), unique=True)
    #ship_owner = db.relationship('User',
    #                             secondary=ship_list,
    #                             backref=db.backref('owner', lazy='dynamic'),
    #                             lazy='dynamic')

    def __repr__(self):
        return self.ship_name

class ShipType(db.Model):
    __tablename__ = 'shiptype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    cnt = db.Column(db.String(12), nullable=False, default="0")
    image = db.Column(db.String(255))
    manufacture = db.Column(db.String(255))
    link = db.Column(db.String(255))
    ship_name = db.relationship('Ship', backref='shiptype', lazy='dynamic')

    def __init__(self, id=None, name=None, cnt="0", image=None, manufacture=None, link=None):
        self.id = id
        self.name = name
        self.cnt = cnt
        self.image = image
        self.manufacture = manufacture
        self.link = link

    def __unicode__(self):
        return self.name