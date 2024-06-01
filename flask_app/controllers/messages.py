from flask_app import app
from flask import render_template, session, redirect, request, flash, url_for
from flask_app.controllers import users, groups, events, messages
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.event import Event
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/messages')
def messages():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user_affiliated = Group.get_by_user_id(data)
    if not user_affiliated:
        flash('You must first affiliate yourself using the "group" button on the top right of the dashboard before you can see messages.')
        return redirect('/')
    user = User.get_by_id(data)
    return render_template('messages.html', user = user)