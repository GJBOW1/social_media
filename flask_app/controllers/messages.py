from flask_app import app
from flask import render_template, session, redirect, request, flash, url_for
from flask_app.controllers import users, groups, events, messages, home
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime

@app.route('/messages')
def messages():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    team_data = {
        'id' : session.get('team_id')
    }
    user_affiliated = Group.get_by_user_id(data)
    if not user_affiliated:
        flash('You must first affiliate yourself using the "group" button on the top right of the dashboard before you can see messages.')
        return redirect('/')
    user = User.get_by_id(data)
    message = Message.get_messages_by_group(team_data)
    return render_template('messages.html', user = user, message = message)

@app.route('/add_message')
def add_message():
    team_data = {
        'id' : session.get('team_id')
    }
    team = Group.get_by_id(team_data)
    return render_template('add_message.html', team = team)

@app.route('/submit_message', methods=["POST"])
def submit_messages():
    data = {
        'message' : request.form.get('message'),
        'user_id' : session.get('user_id'),
        'team_id' : session.get('team_id'),
        'date_time' : '2024-12-25 05:00:00'
    }
    Message.save_messages(data)
    return redirect('/messages')

@app.route('/edit_message/<int:id>')
def edit_message(id):
    if not session.get('user_id'):
        return redirect ('/')
    user_data = {
        'id' : session.get('user_id')
    }
    team_data = {
        'id': session.get('team_id')
    }
    message_data = {
        'id' : id
    }
    user = User.get_by_id(user_data)
    message = Message.get_messages_by_id(message_data)
    team = Group.get_by_id(team_data)
    return render_template('edit_message.html', user = user, message = message, team = team)

@app.route('/submit_edit_message/<int:id>', methods=['POST'])
def submit_messages_edit(id):
    message_data = {
        'id' : id,
        'message' : request.form['message'],
        'user_id' : session.get('user_id'),
        'team_id' : session.get('team_id'),
        'date_time' : '2024-12-25 05:00:00'
    }
    Message.edit_message(message_data)
    return redirect('/messages')

@app.route('/delete_message/<int:id>')
def delete_message(id):
    message_data = {
        'id' : id
    }
    Message.delete_message(message_data)
    return redirect('/messages')