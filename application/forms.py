

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, NumberRange, Optional, Regexp


class LoginForm(FlaskForm):
    login = StringField("Login Id", validators=[InputRequired()],render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired()],render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")


class RegisterationForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()], render_kw={'Placeholder': 'Patient Id'})
    patient_name = StringField("Patient Name*", validators=[InputRequired(), Regexp(regex='^[A-Za-z]+$',message='Name should contain alphabets only')],render_kw={'Placeholder': 'Patient Name'})
    age = IntegerField('Age*', validators=[InputRequired()],render_kw={'Placeholder': 'Patient Id'})
    doa = DateField('Date of Admission*' , validators=[InputRequired()], format='%Y-%m-%d')
    bed_type = SelectField("Bed Type*", validators=[InputRequired()], choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'Placeholder': 'Select'})
    address = TextAreaField("Address*" ,validators=[InputRequired()], render_kw={'Placeholder': 'Enter Address'})
    state = StringField("State*", validators=[InputRequired()],render_kw={'Placeholder': 'State'})
    city = StringField("City*", validators=[InputRequired()],render_kw={'Placeholder': 'City'})
    submit = SubmitField("Register")

class UpdateForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient Id'})
    patient_name = StringField("Patient Name", validators=[Optional(),Regexp(regex='^[A-Za-z]+$',message='Name should contain alphabets only')],render_kw={'Placeholder': 'Patient Name'})
    age = IntegerField("Age", validators=[Optional(),Length(min=3, max=3)],render_kw={'Placeholder': 'Age'})
    doa = DateField("Date of Admission" ,validators=[Optional()] ,format='%Y-%m-%d')
    bed_type = SelectField("Bed Type",  validators=[Optional()],choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'Placeholder': 'Select'})
    address = TextAreaField("Address" ,validators=[Optional()], render_kw={'Placeholder': 'Enter Address'})
    state = StringField("State", validators=[Optional()],render_kw={'Placeholder': 'State'})
    city = StringField("City", validators=[Optional()],render_kw={'Placeholder': 'City'})
    get = SubmitField("Get")
    update = SubmitField("Update")
