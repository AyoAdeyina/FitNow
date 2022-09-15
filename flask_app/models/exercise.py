from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user, workout
from flask import flash, session

class Exercise:
    db = "fitnow"

    def __init__(self, data):
        self.muscle_group = data['muscle_group']
        self.exercise_name = data['exercise_name']
        self.reps = data['reps']
        self.sets = data['sets']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.workout_id = data['workout_id']
        self.id = data['id']


# Create - SQL

    @classmethod
    def create_exercise(cls,data):
        if not cls.validate_exercise(data):
            return False
        query = """
        INSERT INTO exercises (muscle_group, exercise_name, reps, sets, workout_id)
        VALUES (%(muscle_group)s, %(exercise_name)s, %(reps)s, %(sets)s, %(workout_id)s)
        ;"""
        exercise_id = connectToMySQL(cls.db).query_db(query,data)
        return exercise_id


# Read - SQL

    @classmethod
    def get_exercise_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM exercises
        Where id = %(id)s
        ;"""
        exercise = connectToMySQL(cls.db).query_db(query, data)
        print('***********', exercise)
        if exercise:
            exercise = cls(exercise[0])
        return exercise



# Update - SQL

    @classmethod
    def update_exercise_by_id(cls,data):
        if not cls.validate_exercise(data):
            return False
        query = """
        UPDATE exercises 
        SET muscle_group = %(muscle_group)s, exercise_name = %(exercise_name)s, reps = %(reps)s, 
        sets = %(sets)s, updated_at = NOW() 
        WHERE id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return True


# Delete - SQL

    @classmethod
    def destroy_exercise_by_id(cls,id):
        data = {'id' : id}
        query = """
        DELETE FROM exercises 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)



#Validate (staticmethods)

    @staticmethod
    def validate_exercise(data):
        is_valid = True
        if len(data['muscle_group']) < 3:
            flash('Your muscle group name must be atleast two characters long')
            is_valid = False
        if len(data['exercise_name']) < 3:
            flash('Your exercise name must be atleast two characters long')
            is_valid = False
        if len(data['reps']) < 1:
            flash('Your reps must be more than one repetition')
            is_valid = False
        if len(data['sets']) < 1:
            flash('Your sets must be more than one set')
            is_valid = False
        return is_valid