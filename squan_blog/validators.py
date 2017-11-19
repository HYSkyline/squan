# -*- coding:utf-8 -*-

from wtforms.validators import ValidationError


class Mail(object):
    def __init__(self, field, message):
        self.field = field
        self.message = message

    def __call__(self, form, field):
        if (field.data.find('@') > 0 and field.data.find('.') > field.data.find('@')) or field.data == '':
        	pass
        else:
            raise ValidationError(self.message)
