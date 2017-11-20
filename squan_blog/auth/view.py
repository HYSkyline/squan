# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db, avatars
from ..models import User
from .forms import LoginForm, RegistrationForm, InfoEditForm
from ..email import send_mail
import time


@auth.before_app_request
def before_request():
    if (
        current_user.is_authenticated and
        not current_user.mail_confirmed and
        request.endpoint[:] == 'main.secret'
    ):
        return redirect(url_for('auth.mail_unconfirm'))


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
        current_user.prefix = form.userprefix.data
        if not form.email.data:
            current_user.user_mail = form.email.data
            current_user.mail_confirmed = False
            db.session.add(current_user)
            db.session.commit()
            flash(u'信息更新完成')
        elif current_user.user_mail==form.email.data:
            db.session.add(current_user)
            db.session.commit()
            flash(u'信息更新完成')
        else:
            current_user.user_mail = form.email.data
            current_user.mail_confirmed = False
            db.session.add(current_user)
            db.session.commit()
            mail_confirm_token = current_user.generate_mail_confirm_token()
            send_mail(
                current_user.user_mail,
                u'邮箱验证邮件',
                'auth/email/confirm',
                user=current_user,
                token=mail_confirm_token
            )
            flash(u'信息更新完成，验证邮件已送至' + current_user.user_mail)
        return redirect(url_for('.userinfo', username=current_user.username))
    form.birthdate.data = current_user.birthdate
    form.intrtext.data = current_user.intr
    form.email.data = current_user.user_mail
    return render_template('auth/infoedit.html',user=current_user, form=form)

@auth.route('/confirm/<token>')
@login_required
def mail_confirm(token):
    if current_user.mail_confirmed:
        return redirect(url_for('.userinfo', username=current_user.username))
    if current_user.mail_confirm(token):
        flash(u'邮件地址验证完成')
    else:
        flash(u'验证未完成:链接失效或超时，可以重新验证')
    return redirect(url_for('.mail_unconfirm', username=current_user.username))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    mail_confirm_token = current_user.generate_mail_confirm_token()
    send_mail(
        current_user.user_mail,
        u'邮箱验证邮件',
        'auth/email/confirm',
        user=current_user,
        token=mail_confirm_token
    )
    flash(u'新邮件已送达' + current_user.user_mail)
    return redirect(url_for('.userinfo', username=current_user.username))


@auth.route('/mail_unconfirm')
@login_required
def mail_unconfirm():
    if current_user.user_mail:
        return render_template('auth/mail_unconfirmed.html')
    else:
        return redirect(url_for('.infoedit'))
