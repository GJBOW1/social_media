from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, group, event, message, weather_api


class Discussion:
    def __init__(self, data):
        self.id = data['id']
        self.discussion = data['discussion']
        self.date_time = data['date_time']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_id = data['team_id']
        discussions = []


    @classmethod
    def get_discussions_by_group(cls,data):
        query = "SELECT * FROM discussions WHERE team_id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        discussions = []
        for row in results:
            discussions.append(cls(row))
        return discussions 
        
    @classmethod
    def get_discussions_by_id(cls,data):
        query = "SELECT * FROM discussions WHERE id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        return results[0]
    
    @classmethod
    def save_discussions(cls, data):
        query = "INSERT INTO discussions (discussion, date_time, team_id, user_id) VALUES (%(discussion)s, %(date_time)s, %(team_id)s, %(user_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query, data)
    
    @classmethod
    def edit_discussion(cls, data):
        query = "UPDATE discussions SET discussion = %(discussion)s, team_id = %(team_id)s, date_time = %(date_time)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod
    def delete_discussion(cls, data):
        query = "DELETE FROM discussions WHERE ID = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query, data)