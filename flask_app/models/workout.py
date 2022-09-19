from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask_app.models import user, exercise
from flask import flash, session

class Workout:
    db = "fitnow"

    def __init__(self, data):
        self.workout_name = data['workout_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.id = data['id']
        self.exercises = []


# Create - SQL

    @classmethod
    def create_workout(cls,data):
        if not cls.validate_workout(data):
            return False
        query = """
        INSERT INTO workouts (workout_name, user_id)
        VALUES (%(workout_name)s, %(user_id)s)
        ;"""
        workout_id = connectToMySQL(cls.db).query_db(query,data)
        return workout_id




# Read - SQL

    @classmethod
    def get_workout_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM workouts
        lEFT JOIN exercises
        On workouts.id = exercises.workout_id
        Where workouts.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        
        workout=cls(results[0])
        
        for row in results:
            if row["exercises.id"] == None:
                return workout
            exercise_data  = {
                "muscle_group" : row['muscle_group'],
                "exercise_name" : row['exercise_name'],
                "reps" : row['reps'],
                "sets" : row['sets'],
                "created_at" : row['exercises.created_at'],
                "updated_at" : row['exercises.updated_at'],
                "workout_id" : row['workout_id'],
                "id" : row['exercises.id']
            }
            workout.exercises.append(exercise.Exercise(exercise_data))
        print('***********', workout)

        return workout




    @classmethod
    def get_all_workouts(cls, data):
        query = """
        SELECT *
        FROM workouts
        JOIN users
        ON workouts.user_id = users.id
        WHERE workouts.user_id = %(user_id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        all_workouts = []
        print('$$$$$$$$$$$$$$$$$', result)
        if not result:
            return result
        for main_workout in result:
            new_workout = cls(main_workout)
            user_data = {
                'id' : main_workout['users.id'],
                'first_name' : main_workout['first_name'],
                'last_name' : main_workout['last_name'],
                'email' : main_workout['email'],
                'password' : main_workout['password'],
                'user_id' : main_workout['user_id'],
                'created_at' : main_workout['users.created_at'],
                'updated_at' : main_workout['users.updated_at']
            }
            new_workout.exercises = user.User(user_data)
            all_workouts.append(new_workout)
        print('$$$$$$$$$$$$$$', all_workouts)
        return all_workouts



# Update - SQL



# Delete - SQL

    @classmethod
    def destroy_workout_by_id(cls,id):
        data = {'id' : id}
        query = """
        DELETE FROM workouts 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

#Validate (staticmethods)

    @staticmethod
    def validate_workout(data):
        is_valid = True
        if len(data['workout_name']) < 1:
            flash('Your workout name must be at least two characters long')
            is_valid = False
        return is_valid