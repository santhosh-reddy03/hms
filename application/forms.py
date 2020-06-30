

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField,  SelectField, TextAreaField,DateField
from wtforms.validators import InputRequired, Length, NumberRange, Optional, Regexp

from datetime import datetime


class LoginForm(FlaskForm):
    login = StringField("Login Id", validators=[InputRequired()],render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired()],render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")

#from
class GetUser(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[InputRequired(), NumberRange(min=100000000, max=999999999)], render_kw={'Placeholder': 'Patient ID'})
    submit = SubmitField("Get Details")


class RegisterationForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired(),Regexp(regex='^\d{9}$')], render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name*", validators=[InputRequired(), Regexp(regex='^[A-Za-z]+$',message='Only Alphabets allowed')],render_kw={'Placeholder': 'Patient Name'})
    age = IntegerField('Age*', validators=[InputRequired(),NumberRange(min=0,max=999)],render_kw={'Placeholder': 'Patient Id'})
    doa = DateField('Date of Admission*', validators=[InputRequired()], format='%Y-%m-%d',default=datetime.now(),render_kw={'Placeholder': 'yyyy-mm-dd'})
    bed_type = SelectField("Bed Type*", validators=[InputRequired()], choices=[('General', 'General Ward'), ('Semi', 'Semi Sharing'), ('Single', 'Single Room')])
    address = TextAreaField("Address*" ,validators=[InputRequired()], render_kw={'Placeholder': 'Enter Address'})
    state = StringField("State*", validators=[InputRequired(),Regexp(regex='^[a-zA-Z]+$')],render_kw={'Placeholder': 'State'})
    city = StringField("City*", validators=[InputRequired(),Regexp(regex='^[a-zA-Z]+$')],render_kw={'Placeholder': 'City'})
    submit = SubmitField("Register")

class UpdateForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired(),Regexp(regex='^\d{9}$')],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name", validators=[Optional(), Regexp(regex='^[A-Za-z]+$',message='Only Alphabets allowed')],render_kw={'Placeholder': 'Patient Name','readonly':True})
    age = IntegerField("Age", validators=[Optional(),NumberRange(min=0,max=999)],render_kw={'Placeholder': 'Age','readonly':True})

    doa = DateField("Date of Admission" ,validators=[Optional()] ,format='%Y-%m-%d',render_kw={'readonly':True,'Placeholder': 'yyyy-mm-dd'})
    bed_type = SelectField("Bed Type",  validators=[Optional()],choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'Placeholder': 'Select','readonly':True})
    address = TextAreaField("Address" ,validators=[Optional()], render_kw={'Placeholder': 'Enter Address','readonly':True})
    state = StringField("State", validators=[Optional(),Regexp(regex='^[a-zA-Z]+$')],render_kw={'Placeholder': 'State','readonly':True})
    city = StringField("City", validators=[Optional(),Regexp(regex='^[a-zA-Z]+$')],render_kw={'Placeholder': 'City','readonly':True})
    get = SubmitField("Get")
    update = SubmitField("Update")

class DeleteForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name",validators=[Optional()],render_kw={'readonly':True})
    age = IntegerField("Age", validators=[Optional()],render_kw={'Placeholder': 'Age','readonly':True})
    doa = DateField("Date of Admission" ,validators=[Optional()],format='%Y-%m-%d',render_kw={'readonly':True,'Placeholder': 'yyyy-mm-dd'})
    bed_type = SelectField("Bed Type",validators=[Optional()], choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'readonly':True})
    address = TextAreaField("Address" , validators=[Optional()],render_kw={'readonly':True})
    state = StringField("State", validators=[Optional()],render_kw={'readonly':True})
    city = StringField("City", validators=[Optional()],render_kw={'readonly':True})
    get = SubmitField("Get")
    delete = SubmitField("Delete")
class SearchForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()],render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name",validators=[Optional()], render_kw={'readonly':True})
    age = IntegerField("Age",validators=[Optional()],render_kw={'Placeholder': 'Age','readonly':True})
    doa = DateField("Date of Admission" ,validators=[Optional()],format='%Y-%m-%d',render_kw={'readonly':True,'Placeholder': 'yyyy-mm-dd'})
    bed_type = SelectField("Bed Type", validators=[Optional()],  choices=[('GW', 'General Ward'), ('SS', 'Semi Sharing'), ('SR', 'Single Room')],
                               render_kw={'readonly':True})
    address = TextAreaField("Address",validators=[Optional()], render_kw={'readonly':True})
    state = StringField("State", validators=[Optional()],render_kw={'readonly':True})
    city = StringField("City",validators=[Optional()], render_kw={'readonly':True})
    search = SubmitField("Search")
