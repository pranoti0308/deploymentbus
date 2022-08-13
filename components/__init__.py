import psycopg2
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY']='d5fb8c4fa8bd46638da'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yqefznvvaaliyh:87b7668136c621a9d7744bca286dec04f0bf7a654cdedd363b6107cea323ea56@ec2-18-204-142-254.compute-1.amazonaws.com:5432/ddnpvg3bgqvo8e'


#establishing the connection
conn = psycopg2.connect(
   database="ddnpvg3bgqvo8e", user='yqefznvvaaliyh', password='87b7668136c621a9d7744bca286dec04f0bf7a654cdedd363b6107cea323ea56', host='ec2-18-204-142-254.compute-1.amazonaws.com', port= '5432'
)
cursor = conn.cursor()
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
from components import routes
