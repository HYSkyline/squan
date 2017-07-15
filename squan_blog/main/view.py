# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_mail
from . import main
from .form import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            # 名称写入数据库
            # db.session.add(user)
            session['known'] = False
            # 准备发送邮件(当前存在ERRNO:10061错误)
            # if current_app.config['FLASK_ADMIN_EMAIL']:
                # print 'prepare to send email now.'
                # send_mail(
                #     current_app.config['FLASK_ADMIN_EMAIL'],
                #     'New User',
                #     'mail/new_user',
                #     user=user
                # )
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known')
    )