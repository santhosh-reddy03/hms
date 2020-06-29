from application import app
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from sqlalchemy import text
from application.forms import LoginForm, RegisterationForm,UpdateForm,DeleteForm,SearchForm
from application import db
from application.models import Patient
from datetime import datetime
from application.models import Userstore

'''db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='desk_executive', password='desk_executive', user_type='E'))
db.session.add(Userstore(loginid='pharmacist', password='pharmacist', user_type='P'))
db.session.add(Userstore(loginid='diagnostic', password='diagnostic', user_type='D'))
db.session.commit()'''



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
                return redirect(url_for('create_patient'))
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



@app.route('/create_patient', methods=['GET', 'POST'])
def create_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        form = RegisterationForm()
        if form.validate_on_submit():
            #Assumption that same person with same id is not registered
            flash('Patient creation initiated successfully', 'success')
            ssn = form.patient_ssn.data
            name = form.patient_name.data
            age = form.age.data
            doa = form.doa.data
            bed = form.bed_type.data
            address = form.address.data
            state = form.state.data
            city = form.city.data
            db.session.add(Patient(patient_ssn=ssn, patient_name=name, age=age,admission_date=doa,bed_type=bed,address=address,city=city,state=state,status="Active"))
            db.session.commit()
            return redirect(url_for('create_patient'))
        else:
            for key in form.errors:
                flash('Invalid ' + key, 'danger')
        return render_template('create_patient.html', form=form,title='Patient Registeration')
    else:
        flash('You are not logged in ','danger')
        return redirect(url_for('login'))

def set_details(form,ssn_flag):
    sql = text("Select * From patients WHERE patient_ssn = :x ")
    rslt = db.engine.execute(sql, x=form.patient_ssn.data)
    details = [row for row in rslt]
    #redirect(url_for('update_patient'))
    form.patient_ssn.render_kw={"readonly":ssn_flag}
    form.patient_name.data=details[0][2]
    form.age.data=details[0][3]
    obj = datetime.strptime(details[0][4], '%Y-%m-%d').date()
    form.doa.data = obj #not able to change date
    form.bed_type.data=details[0][5]
    form.address.data=details[0][6]
    form.state.data=details[0][7]
    form.city.data=details[0][8]



@app.route('/update_patient',methods=['GET', 'POST'])
def update_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        form = UpdateForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !','warning')
            else:
                if form.get.data:
                    set_details(form,True)

                elif form.update.data:
                    sql = text('UPDATE patients SET patient_name = :n, age = :ag, admission_date = :doa, bed_type = :bt, address = :ad, state = :s, city = :c  WHERE patient_ssn = :ssn')
                    rslt = db.engine.execute(sql, n=form.patient_name.data, ag=int(form.age.data), doa=form.doa.data, bt=form.bed_type.data, ad=form.address.data, s=form.state.data, c=form.city.data,ssn=form.patient_ssn.data)
                    flash('Patient update initiated successfully','success')
                    redirect(url_for('update_patient'))

        else:
            for key in form.errors:
                flash('Invalid ' + key, 'danger')
        return render_template('update_patient.html', form=form,title='Update Patient Details')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        form = DeleteForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !','warning')
            else:
                if form.get.data:
                    set_details(form,True)

                elif form.delete.data:
                    sql = text('UPDATE patients SET status = INACTIVE WHERE patient_ssn = :ssn')
                    rslt = db.engine.execute(sql,ssn=form.patient_ssn.data)
                    flash('“Patient deletion initiated successfully','success')
                    redirect(url_for('delete_patient'))


        else:
            for key in form.errors:
                flash('Invalid ' + key, 'danger')
        return render_template('delete_patient.html', form=form,title='Delete Patient Details')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        #code here
        form = SearchForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !','warning')
            else:
                set_details(form, False)
        else:
            for key in form.errors:
                flash('Invalid ' + key, 'danger')
        return render_template('search_patient.html', form=form,title='Search Patient Details')
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
