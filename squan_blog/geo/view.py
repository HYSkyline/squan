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
import copy


@geo.route('/view', methods=['GET', 'POST'])
def geo_query():
	geo_session_class = sessionmaker(bind=geo_engine)
	geo_session = geo_session_class()
	pt_res = geo_session.query(
		Geopoint.ptid,
		Geopoint.projectname,
		Geopoint.quizee,
		Geopoint.quiztime,
		Geopoint.geopt.ST_AsGeoJSON()
	).all()
	pl_res = geo_session.query(
		Geopolyline.plid,
		Geopolyline.projectname,
		Geopolyline.quizee,
		Geopolyline.quiztime,
		Geopolyline.geopl.ST_AsGeoJSON()
	).all()
	pg_res = geo_session.query(
		Geopolygon.pgid,
		Geopolygon.projectname,
		Geopolygon.quizee,
		Geopolygon.quiztime,
		Geopolygon.geopg.ST_AsGeoJSON()
	).all()

	pt_list = []
	pl_list = []
	pg_list = []
	pt = {}
	pl = {}
	pg = {}
	for each in pt_res:
		pt['ptid'] = each[0]
		pt['projectname'] = each[1]
		pt['quizee'] = each[2]
		pt['quiztime'] = each[3]
		pt['geopt'] = json.loads(each[4])
		pt_list.append(copy.deepcopy(pt))
	for each in pl_res:
		pl['plid'] = each[0]
		pl['projectname'] = each[1]
		pl['quizee'] = each[2]
		pl['quiztime'] = each[3]
		pl['geopl'] = json.loads(each[4])
		pl_list.append(copy.deepcopy(pl))
	for each in pg_res:
		pg['pgid'] = each[0]
		pg['projectname'] = each[1]
		pg['quizee'] = each[2]
		pg['quiztime'] = each[3]
		pg['geopg'] = json.loads(each[4])
		pg_list.append(copy.deepcopy(pg))
	geom = {
		'point': pt_list,
		'polyline': pl_list,
		'polygon': pg_list
	}
	return render_template('geo/geoview.html', geom=geom)


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
					geopg='POLYGON' + '((' + geo_coord.encode('utf-8') + '))'
				)
			)
			geo_session.commit()
		else:
			pass
	return render_template('geo/geoedit.html')