from cms import app
import datetime
from flask import render_template, session, redirect, request, flash, url_for
from .data import USERS
from .data import COURSE


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/profile')

    if request.method == 'POST':
        user_creds = request.form.to_dict()
        user_found = False

        for user in USERS:
            if user_creds["username"] == user['username'] and user_creds['password'] == user['password']:
                session['username'] = user['username']
                session['password'] = user['password']
                session['course'] = user['course']
                flash("Logged in Successfully!")
                return redirect("/profile")
            elif user_creds["username"] == user['username']:
                flash("Invalid Password")
                return redirect("/login")

        # no matching user was found
        flash("Invalid Username")
        return redirect("/login")

    return render_template("login.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/profile')

    if request.method == 'POST':
        data = request.form.to_dict()

        for user in USERS:
            if data['username'] == user['username']:
                flash("This username already exists")
                return redirect("/register")

        if data['password'] != data['confirm-password']:
            flash("Password didn't match")
            return redirect("/register")

        if not data["course"]:
            flash("Please select a course")
            return redirect("/register")

        USERS.append({
            'username': data['username'],
            'password': data['password'],
            'course': data['course']
        })
        # print(USERS)
        flash("Account Created Successfully!")
        return redirect("/login")

    course_names = []
    for c in COURSE:
        course_names.append(c['course'])
    print(course_names)

    return render_template("register.html"
                           , my_options=course_names)


@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop("username")

    return redirect("/login")


@app.route("/profile")
def home():
    if 'username' not in session:
        return redirect("/login")

    return render_template("profile.html")


@app.route("/students")
def students():
    for course in COURSE:
        if course["course"] == session['course']:
            stu_lis = course
            break
    return render_template("student_list.html"
                           , stu_lis=stu_lis)


@app.route("/students/profile/<student_name>", methods=['GET', 'POST'])
def student_profile(student_name):
    quiz_name = request.form.get('name')
    total_marks = request.form.get('t_marks')
    obtained_marks = request.form.get('obt_marks')

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    for course in COURSE:
        if course['course'] == session['course']:
            for student in course["Students"]:
                if student['name'] == student_name:
                    quizes = student['quizes']
                    if quiz_name:
                        new_quiz = {
                            "name": quiz_name,
                            "t_marks": total_marks,
                            "obt_marks": obtained_marks
                        }
                        student['quizes'].append(new_quiz)
                    return render_template("student_profile.html"
                                           , student=student
                                           , quizes=quizes
                                           , current_date=current_date)
    return "Student not found"


