from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, group, event


class Message:
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.date_time = data['date_time']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_id = data['team_id']
        messages = []


    @classmethod
    def get_messages_by_group(cls,data):
        query = "SELECT * FROM messages WHERE team_id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        messages = []
        for row in results:
            messages.append(cls(row))
        return messages 
        
    @classmethod
    def get_messages_by_id(cls,data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        return results
    
    @classmethod
    def save_messages(cls, data):
        query = "INSERT INTO messages (comment, date_time, team_id, user_id) VALUES (%(comment)s, %(date_time)s, %(team_id)s, %(user_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query, data)
    
    
    @classmethod
    def save_message(cls, data):
        query = "INSERT INTO messages (comment, date_time, comment, team_id) VALUES (%(event)s, %(date_time)s, %(comment)s, %(team_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query, data)
    
    @classmethod
    def edit_message(cls, data):
        query = "UPDATE messages SET comment = %(comment)s, date_time = %(date_time)s, team_id = %(team_id)s, user_id = %(user_id)s WHERE id = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod
    def delete_message(cls, data):
        query = "DELETE FROM messages WHERE ID = %(id)s;"
        return connectToMySQL('groupspace_schema').query_db(query, data)