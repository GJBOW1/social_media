from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, group, message


class Event:
    def __init__(self, data):
        self.id = data['id']
        self.date_time = data['date_time']
        self.event= data['event']
        self.comment = data['comment']
        self.team_id = data['team_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.events = []
    
    
    @classmethod
    def get_events_by_group(cls,data):
        query = "SELECT * FROM events WHERE team_id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        events = []
        for event in results:
            events.append(cls(event))
        return events   
        
    @classmethod
    def get_event_by_id(cls,data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_events_by_group(cls,data):
        query = "SELECT * FROM events WHERE team_id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        events = []
        for event in results:
            events.append(cls(event))
        return events   
    
    @classmethod
    def save_event(cls, data):
        query = "INSERT INTO events (event, date_time, comment, team_id) VALUES (%(event)s, %(date_time)s, %(comment)s, %(team_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query, data)
