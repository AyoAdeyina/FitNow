from crypt import methods
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, workout


#CREATE - CONTROLLER

@app.route('/users/register', methods = ["POST"])
def register_users():
    if user.User.create_user(request.form):
        return redirect('/users/profile')
    return redirect ('/')


#READ - CONTROLLER

@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/users/profile')
def profile():
    current_user = user.User.get_user_by_id(session['user_id'])
    all_workouts = workout.Workout.get_all_workouts(session)
    return render_template('profile.html', current_user = current_user, all_workouts = all_workouts)


@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/login', methods= ['POST'])
def login_user():
    if user.User.login(request.form):
        return redirect('/users/profile')
    return redirect('/')



#UPDATE - CONTROLLER




#DELETE - CONTROLLER