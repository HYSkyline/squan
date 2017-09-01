# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User, Quiz
from .forms import LoginForm, RegistrationForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.home'))
		else:
			flash(u'密码错误.')
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
	logout_user()
	flash(u'已退出登录.')
	return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(
			username=form.username.data,
			password=form.password.data
		)
		quiz = Quiz(
			quizee = form.username.data,
			r_score = 0,
			a_score = 0,
			b_score = 0,
			m_score = 0,
			w_score = 0,
			s_score = 0,
			u_score = 0,
			g_score = 0
		)
		db.session.add(user)
		db.session.add(quiz)
		flash(u'注册程序完成，现可登录.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@auth.route('/userinfo/<username>', methods=['GET', 'POST'])
@login_required
def userinfo(username):
	user = User.query.filter_by(username=username).first()
	user_quiz = Quiz.query.filter_by(quizee=username).first()
	return render_template('auth/userinfo.html', user=user, quiz=user_quiz)
