from application import app
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from sqlalchemy import text
from application.forms import LoginForm, GetUser, RegisterationForm, UpdateForm, DeleteForm, SearchForm
from application import db
from datetime import datetime
from application.models import Userstore, Patient, Medicine, MedicineCount, Diagnostics, PatientDiagnostics

# db.drop_all()
# db.create_all()
# db.session.add(Userstore(loginid='desk_executive', password='desk_executive', user_type='E'))
# db.session.add(Userstore(loginid='pharmacist', password='pharmacist', user_type='P'))
# db.session.add(Userstore(loginid='diagnostic', password='diagnostic', user_type='D'))
# db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session['user_type'] == 'E':
            return redirect(url_for('create_patient'))
        elif session['user_type'] == 'P':
            return redirect(url_for('pharmacist'))
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
                return redirect(url_for('pharmacist'))
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


@app.route('/create_patient', methods=["GET", "POST"])
def create_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        form = RegisterationForm()
        if form.validate_on_submit():
            # Assumption that same person with same id is not registered
            ssn = form.patient_ssn.data
            name = form.patient_name.data
            age = form.age.data
            doa = form.doa.data
            bed = form.bed_type.data
            address = form.address.data
            state = form.state.data
            city = form.city.data
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=ssn)
            items = [row[0] for row in rslt]
            if not len(items):
                flash('Patient creation initiated successfully', 'success')
                db.session.add(Patient(patient_ssn=ssn, patient_name=name, age=age, admission_date=doa, bed_type=bed, address=address, city=city, state=state,
                                       status="ACTIVE"))
                db.session.commit()
                return redirect(url_for('create_patient'))
            else:
                flash("SSN ID already exists", 'danger')
        return render_template('create_patient.html', form=form, title='Patient Registeration')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


def set_details(form, ssn_flag=True, kw_flags=True):
    sql = text("Select *  From patients WHERE patient_ssn = :x ")
    rslt = db.engine.execute(sql, x=form.patient_ssn.data)
    # print(rslt)
    details = [row for row in rslt]
    form.patient_ssn.render_kw = {"readonly": ssn_flag}
    form.patient_name.data = details[0][2]
    # for integerfield and datefield values has to be rendered exclusively
    form.age.render_kw = {'value': details[0][3], 'readonly': kw_flags}
    form.age.data = int(details[0][3])
    obj = datetime.strptime(details[0][4], '%Y-%m-%d').date()
    form.doa.render_kw = {'value': obj, 'readonly': kw_flags}
    form.doa.data = obj
    # obj1=obj.strftime('%Y-%m-%d')
    form.bed_type.data = details[0][5]
    form.address.data = details[0][6]
    form.state.data = details[0][7]
    form.city.data = details[0][8]


@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    # Assume that data is updated only after first retrieving the patient data using get button
    if 'user_id' in session and session['user_type'] == 'E':
        # code here
        form = UpdateForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !', 'warning')
            else:
                if form.get.data:                                       # when get button is clicked
                    for field in form:
                        if field.name != 'update' and field.name != 'get':
                            field.render_kw = {"readonly": False}          # making fields editable
                    set_details(form, kw_flags=False)                    # populating fields only ssn is readonly
                elif form.update.data and form.patient_name.data:      # to ensure get has been called
                    empty_field = False
                    for field in form:
                        if not field.data and field.name != 'update' and field.name != 'get':
                            empty_field = True
                            break
                    if not empty_field:                                 # empty field check necessary to ensure no fields are none while updating
                        sql = text('UPDATE patients SET patient_name = :n, age = :ag, admission_date = :doa, bed_type = :bt, address = :ad, state = :s, '
                                   'city = :c  WHERE patient_ssn = :ssn AND status = :state')
                        db.engine.execute(sql, n=form.patient_name.data, ag=int(form.age.data), doa=form.doa.data, bt=form.bed_type.data,
                                                 ad=form.address.data, s=form.state.data, c=form.city.data, ssn=form.patient_ssn.data, state='ACTIVE')
                        flash('Patient update initiated successfully', 'success')
                        return redirect(url_for('update_patient'))       # successful update
                    else:
                        flash('Update unsuccessful empty fields found', 'warning')        # unsuccessful update due to empty fields
                        return redirect(url_for('update_patient'))
                else:
                    flash('Please fill the fields using GET button then click on UPDATE button', 'warning')
                    return redirect(url_for('update_patient'))  # confirming the fields are filled using get
        return render_template('update_patient.html', form=form, title='Update Patient Details')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/delete_patient', methods=['GET', 'POST'])
def delete_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        # code here
        form = DeleteForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !', 'warning')
            else:
                if form.get.data:
                    set_details(form)   # populating fields and all are read only

                elif form.delete.data and form.patient_name.data :          # to ensure get has been called
                    sql = text('UPDATE patients SET status = "INACTIVE" WHERE patient_ssn = :ssn AND status = :state')
                    db.engine.execute(sql, ssn=form.patient_ssn.data, state='ACTIVE')
                    flash('Patient deletion initiated successfully', 'success')
                    return redirect(url_for('delete_patient'))
                else:
                    flash('Please fill the fields using GET button then click on UPDATE button', 'warning')
        return render_template('delete_patient.html', form=form, title='Delete Patient Details')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        # code here
        form = SearchForm()
        if form.validate_on_submit():
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_ssn = :x AND status = :state")
            rslt = db.engine.execute(sql, x=form.patient_ssn.data, state='ACTIVE')
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !','warning')
            else:
                set_details(form, ssn_flag=False)                   # ssn is kept as changeable
        return render_template('search_patient.html', form=form, title='Search Patient Details')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/view_patient')
def view_patient():
    if 'user_id' in session and session['user_type'] == 'E':
        # code here
        rslt = db.engine.execute("SELECT patient_ssn,patient_name,age,address,admission_date,bed_type FROM patients WHERE status = 'ACTIVE' ")
        patients = [row for row in rslt]
        # print(patients)
        return render_template('patient_table.html', rows=patients, title='View Patients')

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


@app.route("/pharm", methods=["GET", "POST"])
def pharmacist():
    if 'user_id' in session and session['user_type'] == 'P':
        form = GetUser()
        if form.validate_on_submit():
            sql = text("SELECT medicine.medicine_name, medicine_track_data.issue_count,medicine.price  FROM medicine_track_data LEFT JOIN medicine ON "
                       "medicine_track_data.medicine_id=medicine.medicine_id UNION SELECT medicine.medicine_name, "
                       "medicine_track_data.issue_count,medicine.price  FROM medicine LEFT JOIN medicine_track_data ON "
                       "medicine.medicine_id=medicine_track_data.medicine_id WHERE patient_id = :x")
            rslt = db.engine.execute(sql, x=form.patient_id.data)
            data = list(rslt)
            sql1 = text("select patient_id, patient_name, age, address, admission_date from patients where patient_id = :x")
            rslt1 = db.engine.execute(sql1, x=form.patient_id.data)
            p_data = list(rslt1)
            if p_data:
                patient_data = p_data[0]
                flash("Patient and medicine data found", "success")
                return render_template('pharma_details.html', data=data, title='Pharmacy', patient_data=patient_data)
            else:
                flash("Patient not found", "danger")
                return redirect(url_for('pharmacist'))
        return render_template('pharmacist.html', form=form, title="Pharmacist")
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route("/issue_meds/<int:patient_id>")
def issue_meds(patient_id=0):
    if 'user_id' in session and session['user_type'] == 'P':
        return render_template('issue_meds.html', patient_id=patient_id)
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/addmeds/<int:patient_id>/<medicine_name>/<int:quantity>')
def addmeds(patient_id=0, medicine_name='', quantity=0):
    if patient_id:
        sql = text("select medicine_id, medicine_name, quantity_available, price from medicine where medicine_name = :x")
        rslt = db.engine.execute(sql, x=medicine_name)
        med_data = list(rslt)
        if med_data:
            medicine_id = med_data[0][0]
            medicinename = med_data[0][1]
            quant = med_data[0][2]
            price = med_data[0][3]
            if int(quant) - quantity > 0:
                db.session.add(MedicineCount(patient_id=patient_id, medicine_id=medicine_id, issue_count=quantity))
                db.session.commit()
                data = {"medicinename": medicinename, "price": price, "quant": quantity}
                sql = text("update medicine set quantity_available = :x where medicine_name = :y")
                db.engine.execute(sql, x=int(quant)-quantity, y=medicine_name)
                return jsonify(data)
            else:
                flash("Medicine are less in quantity, Please enter lower number", "warning")
                return jsonify({"error": "stock not available"})
        else:
            # flash("Medicine doesn't exist", "danger")
            return jsonify({"error": "medicine doesnt exist"})
    else:
        return redirect(url_for('pharmacist'))
