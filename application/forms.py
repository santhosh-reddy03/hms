from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Optional, Regexp, Length
from wtforms import ValidationError

import re

class LoginForm(FlaskForm):
    def password_validator(form, field):
        password =field.data
        while True:
            if (len(password)<10):
                raise ValidationError('Password must have at least 10 characters ')
                break
            elif not re.search("[a-z]", password): #lower case check
                raise ValidationError('Password must contain a lower case character ')
                break
            elif not re.search("[A-Z]", password): #uppercase check
                raise ValidationError('Password must contain a upper case character ')
                break
            elif not re.search("[0-9]", password):  #digit check
                raise ValidationError('Password must contain a digit ')
                break
            elif not re.search("[*.!\@\$%^&:;<>,.?/~_+-=|\(\)\{\}\[\]]", password): #special character check
                raise ValidationError('Password must contain a special character ')
                break
            elif re.search("\s", password):
                raise ValidationError('Password should not contains space character ')
                break
            else:
                break
    login = StringField("Login Id", validators=[InputRequired()], render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired(),password_validator], render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")


class GetUser(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[InputRequired(), NumberRange(min=100000000, max=999999999)], render_kw={'Placeholder': 'Patient ID'})
    submit = SubmitField("Get Details")


class RegisterationForm(FlaskForm):
    patient_ssn = StringField("Patient SSN Id*", validators=[InputRequired()], render_kw={'Placeholder': 'Patient SSN Id'})
    patient_name = StringField("Patient Name*", validators=[InputRequired(), Regexp(regex='^[A-Za-z]+$', message='Name should contain alphabets only')],
                               render_kw={'Placeholder': 'Patient Name'})
    age = IntegerField('Age*', validators=[InputRequired()], render_kw={'Placeholder': 'Patient Id'})
    doa = DateField('Date of Admission*', validators=[InputRequired()], format='%Y-%m-%d', render_kw={'Placeholder': "yyyy-mm-dd"})
    bed_type = SelectField("Bed Type*", validators=[InputRequired()], choices=[('General ward', 'General Ward'), ('Semi sharing', 'Semi Sharing'),
                                                                               ('Single room', 'Single Room')],
                           render_kw={'Placeholder': 'Select'})
    address = TextAreaField("Address*", validators=[InputRequired()], render_kw={'Placeholder': 'Enter Address'})
    state = StringField("State*", validators=[InputRequired(), Regexp(regex='^[a-zA-Z]+$')], render_kw={'Placeholder': 'State'})
    city = StringField("City*", validators=[InputRequired(), Regexp(regex='^[a-zA-Z]+$')], render_kw={'Placeholder': 'City'})
    submit = SubmitField("Register")


class UpdateForm(FlaskForm):
    patient_id = StringField("Patient SSN Id*", validators=[InputRequired(), Regexp(regex=r'^\d{9}$')], render_kw={'Placeholder': 'Patient Id'})
    patient_name = StringField("Patient Name", validators=[Optional(), Regexp(regex='^[A-Za-z]+$', message='Only Alphabets allowed')],
                               render_kw={'Placeholder': 'Patient Name', 'readonly': True})
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=999)], render_kw={'Placeholder': 'Age', 'readonly': True})

    doa = DateField("Date of Admission", validators=[Optional()], format='%Y-%m-%d', render_kw={'readonly': True, 'Placeholder': "yyyy-mm-dd"})
    bed_type = SelectField("Bed Type",  validators=[Optional()], choices=[('General ward', 'General Ward'), ('Semi sharing', 'Semi Sharing'),
                                                                          ('Single room', 'Single Room')],
                           render_kw={'Placeholder': 'Select', 'readonly': True})
    address = TextAreaField("Address", validators=[Optional()], render_kw={'Placeholder': 'Enter Address', 'readonly': True})
    state = StringField("State", validators=[Optional(), Regexp(regex='^[a-zA-Z]+$')], render_kw={'Placeholder': 'State', 'readonly': True})
    city = StringField("City", validators=[Optional(), Regexp(regex='^[a-zA-Z]+$')], render_kw={'Placeholder': 'City', 'readonly': True})
    get = SubmitField("Get")
    update = SubmitField("Update")


class DeleteForm(FlaskForm):
    patient_id = StringField("Patient SSN Id*", validators=[InputRequired()], render_kw={'Placeholder': 'Patient Id'})
    patient_name = StringField("Patient Name", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'Patient Name'})
    age = IntegerField("Age", validators=[Optional()], render_kw={'Placeholder': 'Age', 'readonly': True})
    doa = DateField("Date of Admission", validators=[Optional()], format='%Y-%m-%d', render_kw={'readonly': True, 'Placeholder': "yyyy-mm-dd"})
    bed_type = SelectField("Bed Type", validators=[Optional()], choices=[('General ward', 'General Ward'), ('Semi sharing', 'Semi Sharing'),
                                                                         ('Single room', 'Single Room')], render_kw={'readonly': True})
    address = TextAreaField("Address", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'Address'})
    state = StringField("State", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'State'})
    city = StringField("City", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'City'})
    get = SubmitField("Get")
    delete = SubmitField("Delete")


class SearchForm(FlaskForm):
    patient_id = StringField("Patient SSN Id*", validators=[InputRequired(), Regexp(regex=r'^\d{9}$')], render_kw={'Placeholder': 'Patient Id'})
    patient_name = StringField("Patient Name", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'Patient Name'})
    age = IntegerField("Age", validators=[Optional()], render_kw={'Placeholder': 'Age', 'readonly': True})
    doa = DateField("Date of Admission", validators=[Optional()], format='%Y-%m-%d', render_kw={'readonly': True, 'Placeholder': "yyyy-mm-dd"})
    bed_type = SelectField("Bed Type", validators=[Optional()],  choices=[('General ward', 'General Ward'), ('Semi sharing ', 'Semi Sharing'),
                                                                          ('Single room', 'Single Room')], render_kw={'readonly': True})
    address = TextAreaField("Address", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'Address'})
    state = StringField("State", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'State'})
    city = StringField("City", validators=[Optional()], render_kw={'readonly': True, 'Placeholder': 'City'})
    search = SubmitField("Search")
