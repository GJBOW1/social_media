from flask_app import app
from flask import render_template, session, redirect, request, flash, url_for
from flask_app.controllers import users, groups, events, messages, home
from flask_app.models.user import User
from flask_app.models.group import Group
from flask_app.models.event import Event
from flask_app.models.discussion import Discussion
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime

@app.route('/discussions')
def discussions():
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
    discussion = Discssion.get_discussions_by_group(team_data)
    return render_template('discussions.html', user = user, discussion = discussion)

@app.route('/add_discussion')
def add_discussion():
    team_data = {
        'id' : session.get('team_id')
    }
    team = Group.get_by_id(team_data)
    return render_template('add_discussion.html', team = team)

@app.route('/submit_discussion', methods=["POST"])
def submit_discussions():
    data = {
        'discussion' : request.form.get('discussion'),
        'user_id' : session.get('user_id'),
        'team_id' : session.get('team_id'),
        'date_time' : '2024-12-25 05:00:00'
    }
    discussion.save_discussions(data)
    return redirect('/discussions')

@app.route('/edit_discussion/<int:id>')
def edit_discussion(id):
    if not session.get('user_id'):
        return redirect ('/')
    user_data = {
        'id' : session.get('user_id')
    }
    team_data = {
        'id': session.get('team_id')
    }
    discussion_data = {
        'id' : id
    }
    user = User.get_by_id(user_data)
    discussion = discussion.get_discussions_by_id(discussion_data)
    team = Group.get_by_id(team_data)
    return render_template('edit_discussion.html', user = user, discussion = discussion, team = team)

@app.route('/submit_edit_discussion/<int:id>', methods=['POST'])
def submit_discussions_edit(id):
    discussion_data = {
        'id' : id,
        'discussion' : request.form['discussion'],
        'user_id' : session.get('user_id'),
        'team_id' : session.get('team_id'),
        'date_time' : '2024-12-25 05:00:00'
    }
    discussion.edit_discussion(discussion_data)
    return redirect('/discussions')

@app.route('/delete_discussion/<int:id>')
def delete_discussion(id):
    discussion_data = {
        'id' : id
    }
    discussion.delete_discussion(discussion_data)
    return redirect('/discussions')