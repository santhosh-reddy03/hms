

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,  SelectField, TextAreaField,DateField
from wtforms.validators import InputRequired, Length, NumberRange, Optional, Regexp

from datetime import datetime


class LoginForm(FlaskForm):
    login = StringField("Login Id", validators=[InputRequired()],render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired()],render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")


class RegisterationForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()], render_kw={'Placeholder': 'Patient SSN Id'})
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
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name", validators=[Optional(),Regexp(regex='^[A-Za-z]+$',message='Name should contain alphabets only')],render_kw={'Placeholder': 'Patient Name'})
    age = StringField("Age", validators=[Optional(),Regexp(regex='^\d{1,3}$')],render_kw={'Placeholder': 'Age'})
    doa = DateField("Date of Admission" ,validators=[Optional()] ,format='%Y-%m-%d',default=datetime.now())
    bed_type = SelectField("Bed Type",  validators=[Optional()],choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'Placeholder': 'Select'})
    address = TextAreaField("Address" ,validators=[Optional()], render_kw={'Placeholder': 'Enter Address'})
    state = StringField("State", validators=[Optional()],render_kw={'Placeholder': 'State'})
    city = StringField("City", validators=[Optional()],render_kw={'Placeholder': 'City'})
    get = SubmitField("Get")
    update = SubmitField("Update")

class DeleteForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name", validators=[Optional(),Regexp(regex='^[A-Za-z]+$',message='Name should contain alphabets only')],render_kw={'readonly':True})
    age = StringField("Age", validators=[Optional(),Regexp(regex='^\d{1,3}$')],render_kw={'readonly':True})
    doa = DateField("Date of Admission" ,validators=[Optional()] ,format='%Y-%m-%d',default=datetime.now(),render_kw={'readonly':True})
    bed_type = SelectField("Bed Type",  validators=[Optional()],choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'readonly':True})
    address = TextAreaField("Address" ,validators=[Optional()], render_kw={'readonly':True})
    state = StringField("State", validators=[Optional()],render_kw={'readonly':True})
    city = StringField("City", validators=[Optional()],render_kw={'readonly':True})
    get = SubmitField("Get")
    delete = SubmitField("Delete")
class SearchForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name", validators=[Optional(),Regexp(regex='^[A-Za-z]+$',message='Name should contain alphabets only')],render_kw={'readonly':True})
    age = StringField("Age", validators=[Optional(),Regexp(regex='^\d{1,3}$')],render_kw={'readonly':True})
    doa = DateField("Date of Admission" ,validators=[Optional()] ,format='%Y-%m-%d',default=datetime.now(),render_kw={'readonly':True})
    bed_type = SelectField("Bed Type",  validators=[Optional()],choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'readonly':True})
    address = TextAreaField("Address" ,validators=[Optional()], render_kw={'readonly':True})
    state = StringField("State", validators=[Optional()],render_kw={'readonly':True})
    city = StringField("City", validators=[Optional()],render_kw={'readonly':True})
    search = SubmitField("Search")
