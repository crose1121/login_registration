from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "login_registration"

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DB).query_db(query,data)
        return result

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DB).query_db(query,data)
        return User(result[0])

    @staticmethod
    def validate_user(data): #HOW TO CATCH AN EMPTY PASSWORD FIELD?!?
        is_valid = True

        query = "SELECT * FROM users WHERE email=%(email)s"
        result = connectToMySQL(DB).query_db(query,data)
        if len(result) >= 1:
            is_valid = False
            flash("Email already exists")

        if len(data['first_name']) < 2 or len(data['first_name']) > 255:
            is_valid = False
            flash("Name is too long or short")
        if len(data['last_name']) < 2 or len(data['last_name']) > 255:
            is_valid = False
            flash("Name is too long or short")
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Please enter a valid email")
        if len(data['temp']) < 8:
            is_valid = False
            flash("PW TOO SHORT")
        if 'password' not in data:
            is_valid = False
            flash("Please enter a password")

        return is_valid