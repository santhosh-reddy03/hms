

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    login = StringField("Login Id", validators=[InputRequired()],render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired()],render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")
