# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import quiz
from .. import db
from ..models import User, Quiz
# from ..models import TextQuiz, GeoQuiz
# from .form import TextQuizForm, GeoQuizForm


@quiz.route('/quiz/<projectname>', methods=['GET', 'POST'])
def quizNID(projectname):
	quizs = Quiz.query.filter_by(projectname=projectname).all()
	return render_template('quiz/quizNID.html', quiz=quizs)


@quiz.route('/quizID/<projectName>/<username>', methods=['GET', 'POST'])
@login_required
def quizID(username, projectname):
	user = User.query.filter_by(username=username).first_or_404()
	quizs = Quiz.query.filter_by(projectname=projectname).all()
	if user:
		return render_template('quiz/quizID.html', user=current_user, quiz=quizs)


@quiz.route('/quizchar/<username>', methods=['GET', 'POST'])
@login_required
def quizchar(username):
	user = User.query.filter_by(username=username).first_or_404()
	quizs = Quiz.query.filter_by(projectname='char').all()
	if user:
		return render_template('quiz/quizchar.html', user=current_user, quiz=quizs)
