# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from .. import db, geo_engine
from ..models import User
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


@main.route('/test')
def test():
	return render_template('test.html')
