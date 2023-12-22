from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import group
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthdate = data['birthdate']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.groups = []
    
    @classmethod 
    def save(cls, data):
        query = "INSERT into users (first_name, last_name, email, birthdate, city, state, password) values (%(first_name)s, %(last_name)s, %(email)s, %(birthdate)s, %(city)s, %(state)s, %(password)s);"
        return connectToMySQL('groupspace_schema').query_db(query,data)
    
    @classmethod 
    def get_by_email(cls,data):
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        if len(results) < 1:
            print('false at this point')
            return False
        return cls(results[0])
    
    @classmethod 
    def get_user_by_id(cls,data):
        query = "SELECT * from users WHERE id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        return cls(results[0])
    
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * from users LEFT JOIN teams ON users.id = teams.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('groupspace_schema').query_db(query,data)
        print(results)
        user = cls(results[0])
        return user 

    @classmethod
    def get_by_id_car_and_user(cls):
        query = "SELECT * from users LEFT JOIN cars ON users.id = cars.user_id;"
        results = connectToMySQL('cars_schema').query_db(query)
        user = cls(results[0])
        for row in results:
            car_data = {
                "id" : row["cars.id"],
                "price" : row["price"],
                "model" : row["model"],
                "make" : row["make"],
                "year" : row["year"],
                "description" : row["description"],
                "created_at" : row["cars.created_at"],
                "updated_at" : row["cars.updated_at"],
                "user_id" : row["user_id"]
            }
            # user.cars.append(car.Car(car_data))
        return user 
    
    @staticmethod
    def validate_user_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address')
            is_valid = False
        if not len(user['password']) > 7:
            flash('Password must be greater than 7 characters long.')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters long.")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters long.")
            is_valid = False
        if len(user['city']) < 3:
            flash("City name must be at least 3 characters long.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if not len(user['password']) > 7:
            flash('Password must be greater than 7 characters long.')
            is_valid = False
        return is_valid