# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from .. import db, geo_engine
from ..models import Geopoint, Geopolyline, Geopolygon, GeoBase
from . import geo
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import *
from geoalchemy2.shape import from_shape, to_shape
import json


@geo.route('/base', methods=['GET', 'POST'])
def geo_query():
	geo_session_class = sessionmaker(bind=geo_engine)
	geo_session = geo_session_class()
	pt_res = geo_session.query(Geopoint.geopt.ST_AsGeoJSON()).all()
	pl_res = geo_session.query(Geopolyline.geopl.ST_AsGeoJSON()).all()
	pg_res = geo_session.query(Geopolygon.geopg.ST_AsGeoJSON()).all()
	
	pt = []
	pl = []
	pg = []
	for each in pt_res:
		pt.append(json.loads(each[0])['coordinates'])
	for each in pl_res:
		pl.append(json.loads(each[0])['coordinates'])
	for each in pg_res:
		pg.append(json.loads(each[0])['coordinates'])
	geom = {
		'point': pt,
		'polyline': pl,
		'polygon': pg
	}
	return render_template('geo/geobase.html', geom=geom)
