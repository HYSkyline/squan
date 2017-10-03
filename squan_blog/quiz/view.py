# -*- coding:utf-8 -*-

import random
import time
from flask import render_template, session, redirect, url_for, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from . import quiz
from .. import db
from ..models import User, QuizQuestion, QuizResult
# from ..models import TextQuiz, GeoQuiz
# from .form import TextQuizForm, GeoQuizForm


@quiz.route('/<projectname>', methods=['GET', 'POST'])
def quizNID(projectname):
	quizs = QuizQuestion.query.filter_by(projectname=projectname).all()
	return render_template('quiz/quizNID.html', quiz=quizs)


@quiz.route('/<projectname>/<username>', methods=['GET', 'POST'])
@login_required
def quizID(username, projectname):
	user = User.query.filter_by(username=username).first_or_404()
	quiz_session = QuizQuestion.query.filter_by(projectname=projectname)
	quiz_session_count = quiz_session.count()
	char_num = 3
	if request.method == 'GET':
		if projectname == 'char':
			quizs_id = random.sample(range(quiz_session_count), char_num)
			quizall = quiz_session.all()
			quizs = []
			for i in range(len(quizs_id)):
				quizs.append(quizall[quizs_id[i]])
			return render_template('quiz/quizchar.html', user=current_user, quiz=quizs)
		else:
			quizs = quiz_session.all()
			return render_template('quiz/quizID.html', user=current_user, quiz=quizs)

	if request.method == 'POST':
		if projectname == 'char':
			quiz_session_count = char_num
			char_pre_result = QuizResult.query.filter_by(quizee=username, projectname='char').all()
			if char_pre_result:
				for each in char_pre_result:
					db.session.delete(each)
				db.session.commit()
		for i in range(quiz_session_count):
			quiz_data = QuizResult(
				quizee = current_user.username,
				quiztime = time.time(),
				projectname=projectname,
				quizheading=request.form.get('head' + str(i)),
				quizanswer=request.form.get('head' + str(i) + '-opt')
			)
			db.session.add(quiz_data)
		if projectname == 'char':
			return redirect(url_for('.quizchar_view', username=current_user.username))
		else:
			return redirect(url_for('main.home'))


@quiz.route('/charResult/<username>', methods=['GET'])
@login_required
def quizchar_view(username):
	user = User.query.filter_by(username=username).first_or_404()
	quizchar_data = QuizResult.query.filter_by(
		quizee=username,
		projectname='char'
	).all()
	return render_template('quiz/quizcharResult.html', user=current_user, chardata=quizchar_data)
