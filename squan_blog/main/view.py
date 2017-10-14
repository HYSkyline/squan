# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from .. import db, geo_engine
from ..models import User, Geopoint_test, GeoBase
from ..email import send_mail
from . import main
from .form import NameForm
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import *
from geoalchemy2.shape import from_shape, to_shape
import json


@main.route('/')
def index():
	return render_template('index.html')


@main.route('/home')
def home():
	return render_template('home.html')


@main.route('/secret')
@login_required
def secret():
	return render_template('secret.html')


@main.route('/test', methods=['GET', 'POST'])
def test():
	geo_session_class = sessionmaker(bind=geo_engine)
	geo_session = geo_session_class()
	pt_res = geo_session.query(Geopoint_test.geote.ST_AsGeoJSON()).all()
	pt = []
	for each in pt_res:
		pt.append(json.loads(each[0])['coordinates'])
	return render_template('test.html', geo_res=pt)
