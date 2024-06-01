from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.controllers import home, users, groups, messages
from flask_app.models.group import Group
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_app.models.message import Message

@app.route('/upcoming_events')
def view_events():
    if not session.get('user_id'):
        return redirect('/')
    user_data = {
        'id' : session.get('user_id')
    }
    team_data = {
        'id' : session.get('team_id')
    }
    user_affiliated = Group.get_by_user_id(user_data)
    if not user_affiliated:
        flash('You must first affiliate yourself using the "group" button on the top right of the dashboard before you can see upcoming events.')
        return redirect('/')
    user = User.get_by_id(user_data)
    event = Event.get_events_by_group(team_data) 
    teams = Group.get_by_id(team_data)
    return render_template('upcoming_events.html', user = user, event = event, teams = teams)

@app.route('/add_event')
def add_events():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id'),
        'team_id' : session.get('team_id')
    }
    user = User.get_by_id(data)
    return render_template('add_event.html', user = user)

@app.route('/submit_event', methods=["POST"])
def submit_event():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "event" : request.form['event'],
        "date_time" : request.form['date_time'],
        "comment" : request.form['comment'],
        "team_id" : session.get('team_id')
    }
    Group.save_event(data)
    return redirect('/upcoming_events')

@app.route('/edit_event/<int:id>')
def edit_event(id):
    if not session.get('user_id'):
        return redirect('/')
    user_data = {
        'id' : session.get('user_id')
    }
    team_data = {
        'id' : session.get('team_id')
    }
    data = {
        'id' : id
    }
    user = User.get_by_id(user_data)
    event = Event.get_event_by_id(data)
    teams = Group.get_by_id(team_data)
    return render_template('edit_event.html', user = user, event = event, teams = teams)

@app.route('/submit_edit/<int:id>', methods=['POST'])
def submit_event_edit(id): 
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "id" : id,
        "event" : request.form['event'],
        "date_time" : request.form['date_time'],
        "comment" : request.form['comment'],
        "team_id" : session.get('team_id')
    }
    Group.edit_event(data)
    return redirect('/upcoming_events')

@app.route('/delete_event/<int:id>')
def delete_event(id):
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : id
    }
    Group.delete_event(data)
    return redirect('/upcoming_events')