# -*- coding:utf-8 -*-

import random
import time
from flask import render_template, session, redirect, url_for, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from . import quiz
from .. import db
from ..models import User, QuizQuestion, QuizResult, QuizRef
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
	quiz_ref = QuizRef.query.all()

	quizchar_r_score = 0
	quizchar_a_score = 0
	quizchar_b_score = 0
	quizchar_m_score = 0
	quizchar_w_score = 0
	quizchar_s_score = 0
	quizchar_u_score = 0
	quizchar_g_score = 0
	for quizchar_i in range(len(quizchar_data)):
		for ref_i in range(len(quiz_ref)):
			if quizchar_data[quizchar_i].quizanswer == quiz_ref[ref_i].quizoption:
				quizchar_r_add, quizchar_a_add, quizchar_b_add, quizchar_m_add, quizchar_w_add, quizchar_s_add, quizchar_u_add, quizchar_g_add = quiz_ref[ref_i].refvalue.split('||')
				quizchar_r_score += int(quizchar_r_add)
				quizchar_a_score += int(quizchar_a_add)
				quizchar_b_score += int(quizchar_b_add)
				quizchar_m_score += int(quizchar_m_add)
				quizchar_w_score += int(quizchar_w_add)
				quizchar_s_score += int(quizchar_s_add)
				quizchar_u_score += int(quizchar_u_add)
				quizchar_g_score += int(quizchar_g_add)
	quizchar_result = '||'.join([
		str(quizchar_r_score),
		str(quizchar_a_score),
		str(quizchar_b_score),
		str(quizchar_m_score),
		str(quizchar_w_score),
		str(quizchar_s_score),
		str(quizchar_u_score),
		str(quizchar_g_score)
	])
	user.char_value = quizchar_result

	quizchar_dic = {
		'r': quizchar_r_score,
		'a': quizchar_a_score,
		'b': quizchar_b_score,
		'm': quizchar_m_score,
		'w': quizchar_w_score,
		's': quizchar_s_score,
		'u': quizchar_u_score,
		'g': quizchar_g_score
	}
	quizchar_cal = sorted(quizchar_dic.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	if quizchar_cal[0][1] - quizchar_cal[1][1] < 3:
		if quizchar_cal[1][1] - quizchar_cal[2][1] < 2:
			if quizchar_cal[2][1] - quizchar_cal[3][1] < 1:
				user.char_res = quizchar_cal[0][0] + quizchar_cal[1][0] + quizchar_cal[2][0] + quizchar_cal[3][0]
			else:
				user.char_res = quizchar_cal[0][0] + quizchar_cal[1][0] + quizchar_cal[2][0]
		else:
			user.char_res = quizchar_cal[0][0] + quizchar_cal[1][0]
	else:
		user.char_res = quizchar_cal[0][0]
	db.session.commit()
	return render_template('quiz/quizcharResult.html', user=current_user, chardata=quizchar_data)
