# -*- coding:utf-8 -*-

from flask import Blueprint

geo = Blueprint('geo', __name__)

from . import view
