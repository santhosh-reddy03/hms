from application import app
from flask import render_template, flash, redirect, request, url_for, jsonify, session
from sqlalchemy import text
from application.forms import LoginForm, GetUser, RegisterationForm, UpdateForm, DeleteForm, SearchForm
from application import db
from datetime import datetime, date
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
            return redirect(url_for('diagnostics'))
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
                return redirect(url_for('diagnostics'))
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
            sql = text("SELECT patient_ssn, status FROM patients WHERE patient_ssn = :x ")
            rslt = db.engine.execute(sql, x=ssn)
            items = [row[1] for row in rslt]
            if not len(items) or items[0] == 'INACTIVE':
                flash('Patient creation initiated successfully', 'success')
                if items[0] == 'INACTIVE':   # This ensures that only one entry exists per patient
                    Patient.query.filter_by(patient_ssn=ssn).update(dict(patient_name=name, age=age, admission_date=doa, bed_type=bed, address=address,
                                                                         city=city, state=state, status="ACTIVE"))
                else:
                    db.session.add(Patient(patient_ssn=ssn, patient_name=name, age=age, admission_date=doa, bed_type=bed, address=address, city=city,
                                           state=state, status="ACTIVE"))
                db.session.commit()
                return redirect(url_for('create_patient'))
            else:
                flash("SSN ID already exists", 'danger')
        return render_template('create_patient.html', form=form, title='Patient Registeration')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


def set_details(form, ssn_flag=True, kw_flags=True):
    sql = text("Select *  From patients WHERE patient_id = :x ")
    rslt = db.engine.execute(sql, x=form.patient_id.data)
    # print(rslt)
    details = [row for row in rslt]
    form.patient_id.render_kw = {"readonly": ssn_flag}
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
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_id = :x AND status = :state")
            rslt = db.engine.execute(sql, x=form.patient_id.data, state='ACTIVE')
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
                                          ad=form.address.data, s=form.state.data, c=form.city.data, ssn=form.patient_id.data, state='ACTIVE')
                        flash('Patient update initiated successfully', 'success')
                        return redirect(url_for('update_patient'))       # successful update
                    else:
                        flash('Update unsuccessful empty fields found', 'warning')        # unsuccessful update due to empty fields
                        return redirect(url_for('update_patient'))
                else:
                    flash('Please fill the fields using GET button then click on UPDATE button', 'warning')
                    return redirect(url_for('update_patient'))  # confirming the fields are filled using get
        elif form.patient_name.data:  # This is a necessity as when invalid comes it field gets locked
            for field in form:
                if field.name != 'update' and field.name != 'get':
                    field.render_kw = {"readonly": False}
            form.patient_id.render_kw = {"readonly": True}
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
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_id = :x AND status =:state")
            rslt = db.engine.execute(sql, x=form.patient_id.data, state='ACTIVE')
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !', 'warning')
            else:
                if form.get.data:
                    set_details(form)   # populating fields and all are read only

                elif form.delete.data and form.patient_name.data:          # to ensure get has been called
                    sql = text('UPDATE patients SET status = "INACTIVE" WHERE patient_id = :id AND status = :state')
                    db.engine.execute(sql, id=form.patient_id.data, state='ACTIVE')
                    # removing user specific data from patient_diagnostic_table
                    sql = text('DELETE FROM patient_diagnostics WHERE patient_id =:id ')
                    db.engine.execute(sql, id=form.patient_id.data)
                    # removing user specific data from medicine_track_table
                    sql = text('DELETE FROM medicine_track_data WHERE patient_id =:id ')
                    db.engine.execute(sql, id=form.patient_id.data)
                    db.session.commit()
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
            sql = text("SELECT  patient_ssn FROM patients WHERE patient_id = :x AND status = :state")
            rslt = db.engine.execute(sql, x=form.patient_id.data, state='ACTIVE')
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Patient not found !', 'warning')
            else:
                set_details(form, ssn_flag=False)  # ssn is kept as changeable
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


@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if 'user_id' in session and session['user_type'] == 'E':
        # Assumption no pre booking is allowed
        # After billing the page should be discharged automatically and the patient has be to made inactive
        # Also data from other tables has to be removed
        form = GetUser()
        if form.validate_on_submit():
            bed_price = {'General ward': '2000', 'Single room': '8000', 'Semi sharing': '4000'}
            patient_id = form.patient_id.data
            sql1 = text("select status, patient_id, patient_name, age, address, admission_date, bed_type from patients where patient_id = :x")
            rslt1 = db.engine.execute(sql1, x=patient_id)
            p_data = list(rslt1)
            if p_data:
                if p_data[0][0] == 'ACTIVE':
                    bill = text("SELECT medicine.medicine_name, medicine_track_data.issue_count,medicine.price, "
                                "(medicine.price * medicine_track_data.issue_count) AS Amount FROM medicine_track_data LEFT JOIN medicine ON "
                                "medicine_track_data.medicine_id=medicine.medicine_id WHERE patient_id = :x ")
                    rslt = db.engine.execute(bill, x=patient_id)
                    data = list(rslt)
                    medicine_total_bill = 0
                    if data:
                        for val in data:
                            medicine_total_bill += val[3]
                    bill2 = text("SELECT diagnostics.test_name AS 'Name of the test', diagnostics.charge AS Amount FROM diagnostics "
                                 "LEFT OUTER JOIN  patient_diagnostics ON diagnostics.diagnostics_id=patient_diagnostics.diagnostics_conducted "
                                 "WHERE patient_id = :x ")
                    rslt2 = db.engine.execute(bill2, x=patient_id)
                    data2 = list(rslt2)
                    diagnostics_total_bill = 0
                    if data2:
                        for val in data2:
                            diagnostics_total_bill += val[1]
                    today = date.today()
                    join_date = datetime.strptime(p_data[0][5], '%Y-%m-%d').date()
                    n_days = (today-join_date).days
                    total_charge = [medicine_total_bill, diagnostics_total_bill, n_days*int(bed_price['{}'.format(p_data[0][6])])]
                    return render_template('billing_details.html', meddata=data, patient_data=p_data[0], diagdata=data2, bill=total_charge, days=n_days,
                                           l_day=today, title='Patient Billing')
                else:
                    flash("Patient already discharged", "warning")
                    return redirect(url_for('billing'))
            else:
                flash("Patient not found", "warning")
                return redirect(url_for('billing'))
        else:
            return render_template('billing.html', form=form, title='Patient Billing')
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route("/pharm", methods=["GET", "POST"])
def pharmacist():
    if 'user_id' in session and session['user_type'] == 'P':
        form = GetUser()
        if form.validate_on_submit():
            sql = text("SELECT medicine.medicine_name, medicine_track_data.issue_count,medicine.price  FROM medicine_track_data LEFT JOIN medicine ON "
                       "medicine_track_data.medicine_id=medicine.medicine_id WHERE patient_id = :x")
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
            if int(quant) - quantity >= 0:
                db.session.add(MedicineCount(patient_id=patient_id, medicine_id=medicine_id, issue_count=quantity))
                db.session.commit()
                data = {"medicinename": medicinename, "price": price, "quant": quantity}
                sql = text("update medicine set quantity_available = :x where medicine_name = :y")
                db.engine.execute(sql, x=int(quant)-quantity, y=medicine_name)
                return jsonify(data)
            else:
                # flash("Medicine are less in quantity, Please enter lower number", "warning")
                return jsonify({"error": "stock not available"})
        else:
            # flash("Medicine doesn't exist", "danger")
            return jsonify({"error": "medicine doesnt exist"})
    else:
        return redirect(url_for('pharmacist'))


@app.route('/diagnostics', methods=['GET', 'POST'])
def diagnostics():
    if 'user_id' in session and session['user_type'] == 'D':
        form = GetUser()
        if form.validate_on_submit():
            sql = text("SELECT diagnostics.test_name, diagnostics.charge FROM patient_diagnostics LEFT JOIN diagnostics ON "
                       "patient_diagnostics.diagnostics_conducted=diagnostics.diagnostics_id WHERE patient_id = :x")
            rslt = db.engine.execute(sql, x=form.patient_id.data)
            data = list(rslt)
            sql1 = text("select patient_id, patient_name, age, address, admission_date, bed_type from patients where patient_id = :x")
            rslt1 = db.engine.execute(sql1, x=form.patient_id.data)
            p_data = list(rslt1)
            if p_data:
                patient_data = p_data[0]
                flash("Patient and diagnostic data found", "success")
                return render_template('diagnostic_details.html', data=data, title='Diagnostics', patient_data=patient_data)
            else:
                flash("Patient not found", "danger")
                return redirect(url_for('diagnostics'))
        return render_template('diagnostics.html', form=form, title="Diagnostics")
    else:
        flash('You are not logged in ', 'danger')
        return redirect(url_for('login'))


@app.route('/adddiags/<int:patient_id>/<diag_name>')
def adddiags(patient_id=0, diag_name=''):
    if patient_id:
        sql = text("select diagnostics_id, test_name, charge from diagnostics where test_name = :x")
        rslt = db.engine.execute(sql, x=diag_name)
        diag_data = list(rslt)
        if diag_data:
            diagnostics_id = diag_data[0][0]
            testname = diag_data[0][1]
            charge = diag_data[0][2]
            db.session.add(PatientDiagnostics(patient_id=patient_id, diagnostics_conducted=diagnostics_id))
            db.session.commit()
            data = {"testname": testname, "price": charge}
            return jsonify(data)
        else:
            # flash("Medicine doesn't exist", "danger")
            return jsonify({"error": "diagnostic test doesnt exist"})
    else:
        return redirect(url_for('diagnostics'))
