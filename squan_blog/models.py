# -*- coding:utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from geoalchemy2 import Geometry


class LoginLocation(db.Model):
    __tablename__ = 'loginlocation'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    logintime = db.Column(db.DateTime)
    loginlocation = db.Column(Geometry('POINT'))


class Role(db.Model):
    __tablename__ = 'rolelist'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.INTEGER)
    role_name = db.Column(db.String(32))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'userlist'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('rolelist.role_id'))


    def __repr__(self):
        return '<User %r>' % self.username


    @property
    def password(self):
        raise AttributeError('You should not PASS!')


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
