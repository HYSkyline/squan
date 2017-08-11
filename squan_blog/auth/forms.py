# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Regexp, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(FlaskForm):
	username = StringField(
		u'',
		validators=[Required(u'用户名不能为空'), Length(1,16)],
		render_kw={
			"placeholder": u"用户名",
			"class": "valueInput"
		}
	)
	password = PasswordField(
		u'',
		validators=[Required(u'密码不能为空')],
		render_kw={
			"placeholder": u"密码",
			"class": "valueInput"
		}
	)
	remember_me = BooleanField(u'保持登录状态')
	submit = SubmitField(
		u'登录',
	)

	def validate_username(self, field):
		if not User.query.filter_by(username=field.data).first():
			raise ValidationError(u'此用户名不存在.')


class RegistrationForm(FlaskForm):
	username = StringField(
		u'',
		validators=[
			Required(u'输入用户名'), 
			Length(1, 16),
			Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能由字母+数字+下划线组成.')
		],
		render_kw={
			"placeholder": u"用户名",
			"style": "background-color: transparent;"
		}
	)
	password = PasswordField(
		u'',
		validators=[Required(u'输入密码'), EqualTo('password2', message=u'两次密码需要相同')],
		render_kw={
			"placeholder": u"密码",
			"style": "background-color: transparent;"
		}
	)
	password2 = PasswordField(
		u'',
		validators=[Required(u'再次输入密码')],
		render_kw={
			"placeholder": u"确认密码",
			"style": "background-color: transparent;"
		}
	)
	submit = SubmitField(
		u'确认注册',
		render_kw={
			"style": "background-color: transparent;"
		}
	)

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已被注册')
