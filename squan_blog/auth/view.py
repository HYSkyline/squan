# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db
from ..models import User
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
		db.session.add(user)
		flash(u'注册确认完成，现可登录.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)
