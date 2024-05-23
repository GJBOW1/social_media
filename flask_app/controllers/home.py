from flask_app import app
from flask import render_template, session, redirect, request, flash, url_for
from flask_app.controllers import users, groups
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.event import Event
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
        'id' : session.get('user_id'),
        'team_id' : '9'
        # To-Do: Figure out how to insert the team id number from the session without explicitly writing the number. 
    }
    user = User.get_by_id(data)
    event = Event.get_events_by_group(data)
    print(user)
    # cars = Car.get_all_cars()
    return render_template('dashboard.html', user = user, event = event)

# add this to send to the html:  cars = cars

@app.route('/group')
def group():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    group = Group.get_by_user_id(data)
    return render_template('group_affiliation.html', user = user, group = group)

@app.route('/weather')
def weather():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('weather.html', user = user)

@app.route('/time')
def time():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('time.html', user = user)

@app.route('/messages')
def messages():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('message_board.html', user = user)

@app.route('/discussion_board')
def discussion_board():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('discussion_board.html', user = user)

@app.route('/upcoming_events')
def upcoming_events():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'team_id' : '9'
        # To-Do: Figure out how to insert the team id number from the session without explicitly writing the number. 
    }
    event = Event.get_events_by_group(data)
    return render_template('upcoming_events.html', event = event)

@app.route('/add_event')
def add_events():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('add_event.html', user = user)

@app.route('/photos')
def photos():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('photos.html', user = user)

@app.route('/add_photo')
def add_photo():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    return render_template('add_photo.html', user = user)

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
