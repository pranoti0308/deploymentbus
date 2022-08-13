from components.__init__ import db
from flask import redirect, url_for
from flask_login import UserMixin
from components import db,login_manager
from datetime import datetime
from flask import redirect, url_for 

@login_manager.user_loader
def load_user(user_id):
    return Datas.query.get(user_id)

@login_manager.unauthorized_handler
def unautheorized():
    return redirect(url_for('register'))

    
class Datas(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    # image_file=db.Column(db.String(20),nullable=False,default='default.jpg')
    password=db.Column(db.String(60),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    booking = db.relationship('PassengerInfo', backref='datas')
    
class PassengerInfo(db.Model,UserMixin):
    pid=db.Column(db.Integer,primary_key=True)  
    customer_id=db.Column(db.Integer, db.ForeignKey('datas.id'))
    Cname = db.Column(db.String(20),nullable=False)  
    source = db.Column(db.String(20),nullable=False)
    destination = db.Column(db.String(20),nullable=False)
    price=db.Column(db.Integer,nullable=False)  
    time =  db.Column(db.String(20),nullable=False)
    b_date = db.Column(db.Date,default=datetime.utcnow)
    pname = db.Column(db.String(20),nullable=False)
    seats = db.Column(db.String(20),nullable=False)
    # def __init__(username, email, password):
    #     self.email = email
    #     self.password = password
    
    # def __repr_(self):
    #     return f'{self.username} : {self.email} : {self.date_created.strftime("%d/%m/%y, %H:%M:%S")}'

