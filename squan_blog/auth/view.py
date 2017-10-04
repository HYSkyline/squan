# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db, avatars
from ..models import User, UserQuiz
from .forms import LoginForm, RegistrationForm, InfoEditForm
import time

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
		db.session.add(quiz)
		flash(u'注册程序完成，现可登录.')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)


@auth.route('/userinfo/<username>', methods=['GET', 'POST'])
@login_required
def userinfo(username):
	user = User.query.filter_by(username=username).first()
	if user:
		if user.username == current_user.username:
			return render_template('auth/userview.html', user=user)
		else:
			return render_template('auth/userinfo.html', user=user)
	else:
		pass


@auth.route('/infoedit', methods=['GET', 'POST'])
@login_required
def infoedit():
	form = InfoEditForm()
	if form.validate_on_submit():
		if request.files['avatarimg']:
			avatar_name = request.files['avatarimg'].filename
			avatar_filedata = avatars.save(form.avatarimg.data, folder='/squan/squan_blog/static/img/avatar', name=avatar_name)
			current_user.avatar = request.files['avatarimg'].filename
		current_user.birthdate = form.birthdate.data
		current_user.intr = form.intrtext.data
		db.session.add(current_user)
		flash(u'信息更新完成')
		return redirect(url_for('.userinfo', username=current_user.username))
	form.birthdate.data = current_user.birthdate
	form.intrtext.data = current_user.intr
	return render_template('auth/infoedit.html',user=current_user, form=form)
