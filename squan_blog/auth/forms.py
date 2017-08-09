# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
	username = StringField(
		u'',
		validators=[Required(), Length(1,16)],
		render_kw={
			"placeholder": u"用户名",
			"class": "valueInput"
		}
	)
	password = PasswordField(
		u'',
		validators=[Required()],
		render_kw={
			"placeholder": u"密码",
			"class": "valueInput"
		}
	)
	remember_me = BooleanField(u'保持登录状态')
	submit = SubmitField(
		u'登录',
	)


class RegistrationForm(FlaskForm):
	username = StringField(
		u'',
		validators=[Required(), Length(1, 16)],
		render_kw={
			"placeholder": u"用户名",
			"style": "background-color: transparent;"
		}
	)
	password = PasswordField(
		u'',
		validators=[Required(), EqualTo('password2', message=u'两次密码需要相同')],
		render_kw={
			"placeholder": u"密码",
			"style": "background-color: transparent;"
		}
	)
	password2 = PasswordField(
		u'',
		validators=[Required()],
		render_kw={
			"placeholder": u"确认密码",
			"style": "background-color: transparent;"
		}
	)
	submit = SubmitField(
		u'注册',
		render_kw={
			"style": "background-color: transparent;"
		}
	)

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已被注册')
