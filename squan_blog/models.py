# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from geoalchemy2 import Geography

GeoBase = declarative_base()


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
    avatar = db.Column(db.Text)
    char_value = db.Column(db.Text)
    char_res = db.Column(db.String(4))


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


class UserQuiz(db.Model):
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


class QuizQuestion(db.Model):
    """测试库内的测试题目(含选项)数据"""
    __tablename__ = 'quizquestion'
    quizid = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.Text)
    sponsor = db.Column(db.String(32))
    sponsortime = db.Column(db.Numeric)
    quizheading = db.Column(db.Text)
    quizoption = db.Column(db.Text)


    def __repr__(self):
        return '<Quiz heading: %r>' % self.quizheading


class QuizResult(db.Model):
    """测试库内的测试题目(含选项)数据"""
    __tablename__ = 'quizresult'
    quizresultid = db.Column(db.Integer, primary_key=True)
    quizee = db.Column(db.String(32))
    quiztime = db.Column(db.Numeric)
    projectname = db.Column(db.Text)
    quizheading = db.Column(db.Text)
    quizanswer = db.Column(db.Text)


    def __repr__(self):
        return '<%r in %r title: %r answer %r>' % (self.quizee, self.projectname, self.quizheading, self.quizanswer)


class QuizRef(db.Model):
    """测试库到各指标的简单映射"""
    __tablename__ = 'quizref'
    refid = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.Text)
    quizheading = db.Column(db.Text)
    quizoption = db.Column(db.Text)
    refvalue = db.Column(db.Text)

    def __repr__(self):
        return '<%r option: %r value: %r>' % (self.quizheading, self.quizoption, self.refvalue)


class charQuote():
    def __init__(self, char_dict):
        self.chardict = char_dict


class Geopoint(GeoBase):
    """点类地理数据"""
    __tablename__ = 'geo_point'
    ptid = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.Text)
    quizee = db.Column(db.String(32))
    quiztime = db.Column(db.Numeric)
    geopt = db.Column(Geography(geometry_type='POINT', srid=4326))


class Geopolyline(GeoBase):
    """线类地理数据"""
    __tablename__ = 'geo_polyline'
    plid = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.Text)
    quizee = db.Column(db.String(32))
    quiztime = db.Column(db.Numeric)
    geopl = db.Column(Geography(geometry_type='LINESTRING', srid=4326))


class Geopolygon(GeoBase):
    """面类地理数据"""
    __tablename__ = 'geo_polygon'
    pgid = db.Column(db.Integer, primary_key=True)
    projectname = db.Column(db.Text)
    quizee = db.Column(db.String(32))
    quiztime = db.Column(db.Numeric)
    geopg = db.Column(Geography(geometry_type='POLYGON', srid=4326))
