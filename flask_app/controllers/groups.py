from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.controllers import home, users
from flask_app.models.group import Group
from flask_app.models.user import User

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

@app.route('/create_event', methods=["POST"])
def create_event():
    print("this is the session ID: ", session.get('group_id'))
    data = {
        "event" : request.form['event'],
        "date_time" : request.form['date_time'],
        "comment" : request.form['comment'],
        "team_id" : session.get('group_id')
    }
    Group.save_event(data)
    return redirect('/add_event')