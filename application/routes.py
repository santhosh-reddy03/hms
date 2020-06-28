from application import app
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from sqlalchemy import text
from application.forms import LoginForm
from application import db
from application.models import Patient, Medicine, MedicineCount, Diagnostics, PatientDiagnostics
import datetime
from application.models import Userstore

db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='desk_executive', password='desk_executive', user_type='E'))
db.session.add(Userstore(loginid='pharmacist', password='pharmacist', user_type='P'))
db.session.add(Userstore(loginid='diagnostic', password='diagnostic', user_type='D'))
db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session['user_type'] == 'E':
            return redirect(url_for('create_patient'))
        elif session['user_type'] == 'P':
            return "<h1>pharmacist</h1>"
        elif session['user_type'] == 'D':
            return "<h1>diagnostic</h1>"
    form = LoginForm()
    if form.validate_on_submit():
        sql = text("SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        rslt = db.engine.execute(sql, x=form.login.data, y=form.password.data)
        user_type = [row[0] for row in rslt]
        form.login.data = ''
        if len(user_type) == 0:
            flash('Entered Login ID or Password is Wrong !', 'danger')
        else:
            session['user_id'] = form.login.data
            session['user_type'] = user_type[0]
            if user_type[0] == 'E':
                return redirect(url_for('create_customer'))
            elif user_type[0] == 'P':
                return "<h1>pharmacist</h1>"
            elif user_type[0] == 'D':
                return "<h1>diagnostic</h1>"
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
        session.pop('user_type', None)
        flash('Logged out successfully ', 'success')
    return redirect(url_for('login'))


@app.route('/create_patient')
def create_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        # form = CreatePatient()
        # code here
        return render_template('create_patient.html')

    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/update_patient')
def update_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        pass
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/delete_patient')
def delete_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        pass

    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/search_patient')
def search_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        pass

    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/view_patient')
def view_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        pass

    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/billing')
def billing():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        pass

    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))
