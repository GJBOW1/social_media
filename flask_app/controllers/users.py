from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.controllers import home
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=["POST"])
def registration():
    if User.get_by_email(request.form):
        flash("This email address is already in use.")
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    if not bcrypt.check_password_hash(pw_hash, request.form['confirm_password']):
        flash('Invalid Email and/or Password')
        return redirect('/')
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "birthdate" : request.form['birthdate'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')