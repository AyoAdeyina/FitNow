from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import workout
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

class User:
    db = "fitnow"

    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.id = data['id']
        self.workouts = []


#CREATE

    @classmethod
    def create_user(cls,data):
        if not cls.validate_user_reg_data(data):
            return False
        parsed_data = cls.parse_reg_data(data)
        query = """
        INSERT INTO users(first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, parsed_data)
        print('Created user with id of', user_id)
        session['user_id'] = user_id
        return True




#READ

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT *
        FROM users
        Where email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        print('***********', result)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM users
        Where id = %(id)s
        ;"""
        user = connectToMySQL(cls.db).query_db(query, data)
        print('***********', user)
        if user:
            user = cls(user[0])
        return user


#UPDATE


#DELETE


#Validate (staticmethods)

    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            flash('Your name must be atleast two characters long')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Your name must be atleast two characters long')
            is_valid = False
        if len(data['password']) < 8:
            flash('Your password must contain eight characters and make it a solid one')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if User.get_user_by_email(data['email'].lower()):
            flash('That email is already in use')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Your password does not work')
            is_valid = False
        return is_valid


    @staticmethod
    def parse_reg_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        parsed_data['email'] = data['email'].lower()
        return parsed_data

    @staticmethod
    def login(data):
        main_user = User.get_user_by_email(data['email'].lower())
        if main_user:
            if bcrypt.check_password_hash(main_user.password, data['password']):
                session['user_id'] = main_user.id
                return True
        flash('login information is incorrect')
        return False
