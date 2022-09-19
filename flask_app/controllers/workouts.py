from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, workout, exercise




#CREATE - CONTROLLER

@app.route('/create/workout')
def create_workout():
    
    return render_template('new_workout.html')

@app.route('/create/workout', methods=['POST'])
def finished_workout():
    workout_id = workout.Workout.create_workout(request.form)
    if workout_id:
        return redirect(f'/workout/{workout_id}')
    return redirect('/create/workout')

@app.route('/create/exercise', methods=['POST'])
def finished_exercise():
    exercise_id = exercise.Exercise.create_exercise(request.form)
    return redirect(request.referrer)



#READ - CONTROLLER
@app.route('/workout/<int:id>')
def workout_ex(id):
    this_workout = workout.Workout.get_workout_by_id(id)
    return render_template('new_exercises.html', this_workout = this_workout)




#UPDATE - CONTROLLER

@app.route("/edit/exercises/<int:id>")
def edit_exercise(id):
    old_exercise = exercise.Exercise.get_exercise_by_id(id)
    if not "user_id" in session:
        return redirect("/")
    return render_template("edit_workout.html", old_exercise = old_exercise)

@app.route("/update/exercise", methods = ["POST"])
def update_exercise():
    if exercise.Exercise.update_exercise_by_id(request.form):
        return redirect('/users/profile')
    else:
        return redirect(f'/edit/exercises/{request.form["id"]}')



#DELETE - CONTROLLER

@app.route("/destroy/workouts/<int:id>")
def delete_workout(id):
    if not "user_id" in session:
        return redirect('/')
    workout.Workout.destroy_workout_by_id(id)
    return redirect('/users/profile')


@app.route("/destroy/exercises/<int:id>")
def delete_exercise(id):
    if not "user_id" in session:
        return redirect('/')
    exercise.Exercise.destroy_exercise_by_id(id)
    return redirect('/users/profile')