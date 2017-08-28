# -*- coding:utf-8 -*-

from flask import redirect, request, url_for
from . import api
from .. import db
# from ..models import User, LoginLocation

@api.route('/loginlocation/', methods=['POST'])
def loginlocation():
	print 'ready to write loginlocation to database.'
	# 位置写入数据库的loginlocation表当中
