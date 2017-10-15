# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, request
from .. import db, geo_engine
from ..models import Geopoint, Geopolyline, Geopolygon, GeoBase
from . import geo
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import *
from geoalchemy2.shape import from_shape, to_shape
import json
import time


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


@geo.route('/edit', methods=['GET', 'POST'])
def geo_edit():
	geo_session_class = sessionmaker(bind=geo_engine)
	geo_session = geo_session_class()
	if request.method == 'POST':
		geo_type = request.form.get('geoType')
		geo_coord = request.form.get('geoCoordinate')

		if geo_type == 'POINT':
			geo_session.add(
				Geopoint(
					projectname='init',
					quizee='HYSkyline',
					quiztime=time.time(),
					geopt=geo_type + '(' + geo_coord.encode('utf-8') + ')'
				)
			)
			geo_session.commit()
		elif geo_type == 'LINESTRING':
			geo_session.add(
				Geopolyline(
					projectname='init',
					quizee='HYSkyline',
					quiztime=time.time(),
					geopl=geo_type + '(' + geo_coord.encode('utf-8') + ')'
				)
			)
			geo_session.commit()
		elif geo_type == 'POLYGON':
			geo_session.add(
				Geopolygon(
					projectname='init',
					quizee='HYSkyline',
					quiztime=time.time(),
					geopg='MULTIPOLYGON' + '(((' + geo_coord.encode('utf-8') + ')))'
				)
			)
			geo_session.commit()
		else:
			pass
	return render_template('geo/geoedit.html')