from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.controllers import home, users, messages, events
from flask_app.models.group import Group
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.event import Event

@app.route('/group')
def view_group():
    if not session.get('user_id'):
        return redirect('/')
    data = {
        'id' : session.get('user_id')
    }
    user = User.get_by_id(data)
    group = Group.get_by_user_id(data)
    return render_template('group_affiliation.html', user = user, group = group)

@app.route('/create_group', methods=["POST"])
def create_group():
    if Group.get_by_group_name(request.form):
        flash("This group name is already in use.")
        return redirect('/')
    if not Group.validate_group(request.form):
        return redirect('/')
    data = {
        "group_name" : request.form['group_name'],
        "description" : request.form['description'],
        "user_id" : session.get('user_id')
    }
    group_id = Group.save(data)
    session['group_id'] = group_id
    return redirect('/dashboard')

@app.route('/view/group/<int:id>')
def edit_group(id):
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "id": id
    }
    group = Group.get_by_id(data)
    return render_template('update_group.html', group = group)

@app.route('/update/group/<int:id>', methods=["POST"])
def update_group(id):
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "id": id,
        "group_name" : request.form['group_name'],
        "description" : request.form['description']
    }
    Group.update_by_id(data)
    return redirect('/group')
    
@app.route('/delete/group/<int:id>')
def delete_group(id):
    if not session.get('user_id'):
        return redirect('/')
    data = {
        "id": id
    }
    Group.delete_by_id(data)
    return redirect('/group')
