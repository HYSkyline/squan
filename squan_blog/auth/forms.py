# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
	username = StringField(u'用户名', validators=[Required()])
	password = PasswordField(u'密码', validators=[Required()])
	remember_me = BooleanField(u'保持登录状态')
	submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
	username = StringField(u'用户名', validators=[Required(), Length(1, 32)])
	password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message=u'两次密码需要相同')])
	password2 = PasswordField(u'确认密码', validators=[Required()])
	submit = SubmitField(u'注册')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已被注册')
