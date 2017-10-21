# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app, request
from flask_login import login_required, current_user
from .. import db, geo_engine
from ..models import Geopoint, Geopolyline, Geopolygon, GeoBase
from . import geo
from sqlalchemy.orm import sessionmaker
from geoalchemy2.functions import *
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point, LineString, Polygon
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


@geo.route('/<project_name>', methods=['GET', 'POST'])
@login_required
def geo_edit(project_name):
	geo_session_class = sessionmaker(bind=geo_engine)
	geo_session = geo_session_class()
	if request.method == 'GET':
		pt_res = geo_session.query(
			Geopoint.ptid,
			Geopoint.projectname,
			Geopoint.quizee,
			Geopoint.quiztime,
			Geopoint.geopt.ST_AsGeoJSON()
		).filter_by(projectname=project_name).all()
		pl_res = geo_session.query(
			Geopolyline.plid,
			Geopolyline.projectname,
			Geopolyline.quizee,
			Geopolyline.quiztime,
			Geopolyline.geopl.ST_AsGeoJSON()
		).filter_by(projectname=project_name).all()
		pg_res = geo_session.query(
			Geopolygon.pgid,
			Geopolygon.projectname,
			Geopolygon.quizee,
			Geopolygon.quiztime,
			Geopolygon.geopg.ST_AsGeoJSON()
		).filter_by(projectname=project_name).all()
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
		return render_template('geo/geoedit.html', geom=geom)
	if request.method == 'POST':
		geo_id = long(float(request.form.get('geoId')))
		geo_projectname = project_name
		geo_quizee = current_user.username
		geo_type = request.form.get('geoType')
		geo_coord = request.form.get('geoCoordinate')
		geo_event = request.form.get('geoEvent')
		print ''
		print ''
		print geo_type.encode('utf-8') + ' ' + str(geo_id) + '  processing.'
		print ''
		print ''
		if geo_event == 'DELETED':
			if geo_type == 'POINT':
				pt_res = geo_session.query(Geopoint).filter_by(ptid=geo_id).first()
				geo_session.delete(pt_res)
			elif geo_type == 'LINESTRING':
				pl_res = geo_session.query(Geopolyline).filter_by(plid=geo_id).first()
				geo_session.delete(pl_res)
			elif geo_type == 'POLYGON':
				pg_res = geo_session.query(Geopolygon).filter_by(pgid=geo_id).first()
				geo_session.delete(pg_res)
		else:
			if geo_type == 'POINT':
				pt_res = geo_session.query(Geopoint).filter_by(ptid=geo_id).first()
				if pt_res:
					pt_lng, pt_lat = geo_coord.encode('utf-8').split(' ')
					pt_res.geopt = from_shape(Point(float(pt_lng), float(pt_lat)), srid=4326)
				else:
					geo_session.add(
						Geopoint(
							ptid=geo_id,
							projectname=geo_projectname,
							quizee=geo_quizee,
							quiztime=time.time(),
							geopt=geo_type + '(' + geo_coord.encode('utf-8') + ')'
						)
					)
			elif geo_type == 'LINESTRING':
				pl_res = geo_session.query(Geopolyline).filter_by(plid=geo_id).first()
				if pl_res:
					polyline_point_list = []
					for each_point in geo_coord.encode('utf-8').split(','):
						pt_lng, pt_lat = each_point.split(' ')
						polyline_point_list.append((float(pt_lng), float(pt_lat)))
					pl_res.geopl = from_shape(LineString(polyline_point_list), srid=4326)
				else:
					geo_session.add(
						Geopolyline(
							plid=geo_id,
							projectname=geo_projectname,
							quizee=geo_quizee,
							quiztime=time.time(),
							geopl=geo_type + '(' + geo_coord.encode('utf-8') + ')'
						)
					)
			elif geo_type == 'POLYGON':
				pg_res = geo_session.query(Geopolygon).filter_by(pgid=geo_id).first()
				if pg_res:
					polygon_point_list = []
					for each_point in geo_coord.encode('utf-8').split(',')[:-1]:
						pt_lng, pt_lat = each_point.split(' ')
						polygon_point_list.append((float(pt_lng), float(pt_lat)))
					pg_res.geopg = from_shape(Polygon(polygon_point_list), srid=4326)
				else:
					geo_session.add(
						Geopolygon(
							pgid=geo_id,
							projectname=geo_projectname,
							quizee=geo_quizee,
							quiztime=time.time(),
							geopg='POLYGON' + '((' + geo_coord.encode('utf-8') + '))'
						)
					)
			else:
				pass
		geo_session.commit()
	return ('', 204)