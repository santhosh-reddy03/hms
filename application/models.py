from application import db

#userstore model
class Userstore(db.Model):
    __tablename__ = 'userstore'
    loginid = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    user_type = db.Column(db.String(64))
