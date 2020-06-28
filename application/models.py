from application import db

# userstore model


class Userstore(db.Model):
    __tablename__ = 'userstore'
    loginid = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    user_type = db.Column(db.String(64))


class Patient(db.Model):
    __tablename__ = "patients"
    patient_ssn = db.Column(db.String(64), primary_key=True)
    patient_id = db.Column(db.Integer(), unique=True, index=True)
    patient_name = db.Column(db.String(64))
    age = db.Column(db.Integer())
    admission_date = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))
    bed_type = db.Column(db.String(64))
    address = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    status = db.Column(db.String(64))
    medicines = db.relationship('Address', backref='person', lazy=True)


class MedicineCount(db.Model):
    __tablename__ = "medicine_track_data"
    patient_id = db.Column(db.Integer(), db.ForeignKey('patients.patient_id'))
    patients = db.relationship("Patient", foreign_keys=[patient_id])
    medicine_id = db.Column(db.Integer(), db.ForeignKey("medicine.medicine_id"))
    medicine = db.relationship("Medicine", foreign_key=[medicine_id])
    issue_count = db.Column(db.Integer())


class Medicine(db.Model):
    __tablename__ = "medicine"
    medicine_id = db.Column(db.Integer(), primary_key=True)
    medicine_name = db.Column(db.String(64), unique=True)
    quantity_available = db.Column(db.Integer())
    price = db.Column(db.Integer())


class Diagnostics(db.Model):
    __tablename__ = "diagnostics"
    diagnostics_id = db.Column(db.Integer(), primary_key=True)
    test_name = db.Column(db.String(64), unique=True)
    charge = db.Column(db.Integer())


class PatientDiagnostics(db.Model):
    __tablename__ = "patient_diagnostics"
    patient_id = db.Column(db.Integer(), db.ForeignKey('patients.patient_id'))
    patients = db.relationship("Patient", foreign_key=[patient_id])
    diagnostics_conducted = db.Column(db.Integer(), db.ForeignKey('diagnostics.diagnostics_id'))
    diagnostics = db.relationship("Diagnostics", foreign_key=[diagnostics_conducted])
