from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('Your name:', validators=[Required()])
    submit = SubmitField('Submit')
