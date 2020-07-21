from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name= StringField('name', validators=[Required()])
    submit = SubmitField('제출')

