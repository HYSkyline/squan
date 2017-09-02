# -*- coding:utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from geoalchemy2 import Geometry


class Role(db.Model):
    __tablename__ = 'rolelist'
    rid = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.INTEGER)
    role_name = db.Column(db.String(32))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.role_name


class User(UserMixin, db.Model):
    __tablename__ = 'userlist'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('rolelist.role_id'))
    birthdate = db.Column(db.Date)
    intr = db.Column(db.Text)
    prefix = db.Column(db.Boolean)


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


    def get_id(self):
        try:
            return unicode(self.uid)
        except AttributeError:
            raise NotImplementedError('No id attribute - override get_id()')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Quiz(db.Model):
    """用户的测试信息"""
    __tablename__ = 'userquiz'
    qid = db.Column(db.Integer, primary_key=True)
    quizee = db.Column(db.Text)
    quiz_rec = db.Column(db.String(4))
    r_score = db.Column(db.Integer)
    a_score = db.Column(db.Integer)
    b_score = db.Column(db.Integer)
    m_score = db.Column(db.Integer)
    w_score = db.Column(db.Integer)
    s_score = db.Column(db.Integer)
    u_score = db.Column(db.Integer)
    g_score = db.Column(db.Integer)


    def __repr__(self):
        return '<Quizee %r>' % self.quizee
