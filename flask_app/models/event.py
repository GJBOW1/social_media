from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, group


class Event:
    def __init__(self, data):
        self.id = data['id']
        self.date_time = data['date_time']
        self.event= data['event']
        self.comment = data['comment']
        self.team_id = data['team_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    @classmethod
    def get_events_by_group(cls,data):
        query = "SELECT * FROM events WHERE team_id = %(team_id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        print(results)
        # events = []
        # for event in results:
        #     events.append(cls(event))
        # print(events)
        # return events   
        return results[0]
    
    @classmethod
    def save_event(cls, data):
        query = "INSERT INTO events (event, date_time, comment, team_id) VALUES (%(event)s, %(date_time)s, %(comment)s, %(team_id)s);"
        return connectToMySQL('groupspace_schema').query_db(query, data)
