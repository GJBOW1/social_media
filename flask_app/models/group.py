from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, group


class Group:
    def __init__(self, data):
        self.id = data['id']
        self.group_name = data['group_name']
        self.description= data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.groups = []
    
    @classmethod 
    def save(cls, data):
        query = "INSERT into teams (group_name, description, user_id) values (%(group_name)s, %(description)s, %(user_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod
    def add_member(cls,data):
        query = "INSERT into teams (user_id) values (%(id)s);"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod 
    def get_by_group_name(cls,data):
        query = "SELECT * FROM teams WHERE group_name = %(group_name)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        print(results)
        if len(results) < 1:
            print('false at this point for group that already exists with this name')
            return False
        return cls(results[0])
    
    @classmethod 
    def get_by_user_id(cls,data):
        query = "SELECT * FROM teams WHERE user_id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod 
    def get_by_id(cls,data):
        query = "SELECT * FROM teams WHERE id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_by_id(cls,data):
        query = "UPDATE teams SET group_name = %(group_name)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod 
    def delete_by_id(cls,data):
        query = "DELETE FROM teams WHERE id = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query,data)

    @staticmethod
    def validate_group(group):
        is_valid = True
        if len(group['group_name']) < 3:
            flash("Group name must be at least 3 characters long.")
            is_valid = False
        if len(group['description']) < 5:
            flash("Description must be at least 5 characters long.")
            is_valid = False
        return is_valid