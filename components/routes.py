import email
from flask import Flask, render_template, url_for,redirect,flash,request
from components import forms,app,db,bcrypt,conn
from components.forms import RegistrationForm,LoginForm
from components.models import Datas,PassengerInfo
from components import app, db
from components.forms import RegistrationForm
from flask_login import login_required, login_user,logout_user,current_user
from datetime import datetime

@app.route('/')
def homepage():
    return render_template('homepage.html',title='Home Page')

@app.route('/about')
def about():
    return render_template('About.html',title='About')

@app.route('/account')
@login_required
def account():
    id = current_user.id
    cursor = conn.cursor()
    cursor.execute("select * from passenger_info")
    info = cursor.fetchall()
    user = PassengerInfo.query.filter_by(customer_id = id).all()
    return render_template('Account.html',title='Account',info=info,user=user)

@app.route('/register',methods=['POST','GET'])
def register():
   if current_user.is_authenticated:
    return redirect(url_for('account'))
   form=RegistrationForm()
   if form.validate_on_submit():
    encrypted_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    email = form.email.data
    exist = Datas.query.filter_by(email=email).first()
    if exist:
        flash(f'{form.email.data} already exist!!!', category='danger')
    else:
        users=Datas(username=form.username.data,email=form.email.data,password=encrypted_password)
        db.session.add(users)
        db.session.commit()
        flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login'))

   return render_template('register.html',title='Register',form=form)



@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=Datas.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash(f'Login successfully for {form.email.data}',category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login failed for {form.email.data}',category='danger')
    return render_template('login.html',title='Login',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/booking',methods=['POST','GET'])
def booking():
    if request.method == 'POST':
        source = request.form["source"]
        destination = request.form["destination"]
        cursor = conn.cursor()
        cursor.execute("select * from businfo where source='"+source+"' and destination='"+destination+"'")
        info = cursor.fetchall()
        print(len(info))
        if len(info) == 0 :
            flash(f'Please enter proper source and destination', category='danger')
            return render_template('booking.html')
        else:
            return render_template('booking.html',info=info)
    return render_template('booking.html')
    

@app.route('/passengerInfo',methods=['POST','GET'])
@login_required
def passangerInfo():
    if request.method == 'POST':
        idVal = request.form['a']
        cursor = conn.cursor()
        cursor.execute("select * from businfo where user_id='"+idVal+"'")
        info = cursor.fetchall()
        return render_template('passengerInfo.html',info=info)
    return render_template('passengerInfo.html')

@app.route('/payment',methods=['POST','GET'])
@login_required
def payment():
        if request.method == 'POST':
            customer = request.form["customer"]
            print(customer)
            company_name = request.form["company_name"]
            source = request.form["source"]
            destination = request.form["destination"]
            price = int(request.form["price"])
            time = request.form["time"]
            date = request.form["date"]
            p_name = request.form["p_name"]
            no_seats = int(request.form["no_seats"])
            total_price = price * no_seats
            cus_info=PassengerInfo(customer_id=customer,Cname=company_name,source=source,destination=destination,price=total_price,time=time,b_date=date,pname=p_name,seats=no_seats)
            db.session.add(cus_info)
            db.session.commit()
            return render_template('payment.html',price=total_price)
        else:
          return '<h1>Can not access payment page directly </h1>'
@app.route('/delete/<int:id>')
def delete(id):
    data = PassengerInfo.query.filter_by(customer_id=id).first()
    booking_date =  data.b_date
    print('msg',booking_date)
    now = datetime.now()
    print('msg',now.date())
    today_date = now.date()
    if booking_date == today_date or booking_date < today_date:
        flash(f'You can not cancel {data.source} to {data.destination} booking!!!', category='danger')
        return redirect("/account")        
    else:
        db.session.delete(data)
        db.session.commit()
        return redirect("/account")
        


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method=='POST':
        name = request.form['name']
        query = Datas.query.filter_by(id=id).first()
        query.username = name
        db.session.add(query)
        db.session.commit()
        return redirect("/account")
    return render_template('update.html')

@app.route('/contactus')
def contactus():
    return render_template('ContactUs.html',title='Contact Us')

@app.route('/success',methods=['POST','GET'])
def success():
    if request.method=='POST':
        return render_template('success.html')

@app.errorhandler(404)
def handle_global_error(e):
    return redirect(url_for('homepage'))

