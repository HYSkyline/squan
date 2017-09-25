# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import quiz
from .. import db
from ..models import User
# from ..models import TextQuiz, GeoQuiz
# from .form import TextQuizForm, GeoQuizForm


@quiz.route('/charquiz/<username>', methods=['GET', 'POST'])
@login_required
def charquiz(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user:
		return render_template('quiz/charquiz.html', user=current_user)

