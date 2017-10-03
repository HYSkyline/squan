# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateField, TextField, TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Required, Regexp, Length, Email, EqualTo
from wtforms import ValidationError
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash


class quizcharForm(FlaskForm):
	username = StringField(
		u'',
		validators=[Required(u'选项不能为空')],
		render_kw={
			"placeholder": u"测试选项内容"
		}
	)

	submit = SubmitField(
		u'提交',
	)
