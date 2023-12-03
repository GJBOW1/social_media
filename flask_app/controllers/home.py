from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.controllers import users
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    if session.get('user_id'):
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    print(user)
    # cars = Car.get_all_cars()
    return render_template('dashboard.html', user = user)

# add this to send to the html:  cars = cars


@app.route('/login', methods=["POST"])
def login():
    data = {
        'email' : request.form['email'],
        'password' : request.form['password']
    }
    if not User.validate_user_login(data):
        return redirect('/')
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email and/or Password')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email and/or Password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    print(session['user_id'])
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
