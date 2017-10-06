# -*- coding:utf-8 -*-

import random
import time
import sys
from flask import render_template, session, redirect, url_for, current_app, request
from flask_login import login_user, logout_user, login_required, current_user
from . import quiz
from .. import db
from ..models import User, QuizQuestion, QuizResult, QuizRef, charQuote
# from ..models import TextQuiz, GeoQuiz
# from .form import TextQuizForm, GeoQuizForm


reload(sys)
sys.setdefaultencoding('utf-8')


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
	char_num = 10
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
		# 	char_pre_result = QuizResult.query.filter_by(quizee=username, projectname='char').all()
		# 	if char_pre_result:
		# 		for each in char_pre_result:
		# 			db.session.delete(each)
		# 		db.session.commit()
		for i in range(quiz_session_count):
			quiz_data = QuizResult(
				quizee = current_user.username,
				quiztime = time.time(),
				projectname=projectname,
				quizheading=request.form.get('head' + str(i)),
				quizanswer=request.form.get('head' + str(i) + '-opt').lstrip().rstrip()
			)
			db.session.add(quiz_data)
		if projectname == 'char':
			return redirect(url_for('.quizchar_view', username=current_user.username))
		else:
			return redirect(url_for('main.home'))


@quiz.route('/charResult/<username>', methods=['GET'])
@login_required
def quizchar_view(username):
	char_num = 10
	user = User.query.filter_by(username=username).first_or_404()
	quizchar_data = QuizResult.query.filter_by(
		quizee=username,
		projectname='char'
	).all()
	quiz_ref = QuizRef.query.all()

	char_quote_file = open('charquote.txt', 'r')
	charquote_content = char_quote_file.readlines()
	char_quote_file.close()
	char_dict = {}
	for each in charquote_content:
		char_code, char_quote, char_quoter, char_origin, char_intr = each.split('\t')
		char_dict[char_code] = [char_quote, char_quoter, char_origin, char_intr[:-1]]
	quizchar_quote = charQuote(char_dict)

	quiztime_list = []
	for i in range(0, len(quizchar_data), char_num):
		quiztime_list.append(quizchar_data[i].quiztime)
	quiztime_count = len(quizchar_data) / char_num

	quizchar_score_strlist=[]
	for time_i in range(quiztime_count):
		quizchar_score = [0, 0, 0, 0, 0, 0, 0, 0]
		for quizchar_i in range(char_num * time_i, char_num * (time_i + 1)):
			for ref_i in range(len(quiz_ref)):
				if quizchar_data[quizchar_i].quizheading == quiz_ref[ref_i].quizheading and quizchar_data[quizchar_i].quizanswer == quiz_ref[ref_i].quizoption:
					quizchar_add = quiz_ref[ref_i].refvalue.split('||')
					for score_i in range(len(quizchar_score)):
						quizchar_score[score_i] += int(quizchar_add[score_i])
		quizchar_score_str = []
		for str_i in range(len(quizchar_score)):
			quizchar_score_str.append(str(quizchar_score[str_i]))
		quizchar_score_strlist.append([int(quiztime_list[time_i]), quizchar_score])
	
	quizchar_dic = {
		'R': quizchar_score[0],
		'A': quizchar_score[1],
		'B': quizchar_score[2],
		'M': quizchar_score[3],
		'W': quizchar_score[4],
		'S': quizchar_score[5],
		'U': quizchar_score[6],
		'G': quizchar_score[7]
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

	user.char_value = '||'.join(quizchar_score_str)
	db.session.commit()
	return render_template('quiz/quizcharResult.html', user=current_user, chardata=quizchar_score_strlist, charquote=quizchar_quote)
