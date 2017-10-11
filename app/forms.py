#from flask.ext.wtf import Form
from flask_wtf import FlaskForm
#from flaskForm import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=4, max=140)])
