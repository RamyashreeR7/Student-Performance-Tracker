# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Grade, Subject
from tracker import StudentTracker
from config import DATABASE_URI

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "change-me"  # set from env in prod
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Initialize default subjects if none exist
        if Subject.query.count() == 0:
            default_subjects = ["Math", "Science", "English"]
            for subject_name in default_subjects:
                subject = Subject(name=subject_name)
                db.session.add(subject)
            db.session.commit()
    return app

app = create_app()
tracker = StudentTracker()

@app.route("/")
def index():
    students = tracker.list_students()
    topper_results = {}
    avg_results = {}

    subjects = tracker.get_subjects()
    for sub in subjects:
        topper_results[sub] = None
        avg_results[sub] = None

    return render_template(
        "index.html",
        students=students,
        subjects=subjects,
        topper_results=topper_results,
        avg_results=avg_results
    )


@app.route("/students")
def students():
    students = tracker.list_students()
    return render_template("students.html", students=students)

@app.route("/student/<roll>")
def student_details(roll):
    w = tracker.view_student_details(roll)
    if not w:
        flash("Student not found.", "danger")
        return redirect(url_for("students"))
    return render_template("student_details.html", s=w)

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll", "").strip()
        if not name or not roll:
            flash("Name and roll number are required.", "warning")
            return redirect(url_for("add_student"))
        if tracker.add_student(name, roll):
            flash("Student added.", "success")
            return redirect(url_for("students"))
        else:
            flash("Roll number already exists.", "danger")
            return redirect(url_for("add_student"))
    return render_template("add_student.html")

@app.route("/add-grade", methods=["GET", "POST"])
def add_grade():
    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        subject = request.form.get("subject", "").strip()
        try:
            score = float(request.form.get("score", ""))
        except ValueError:
            flash("Enter a valid score.", "warning")
            return redirect(url_for("add_grade"))
        if tracker.add_grade(roll, subject, score):
            flash("Grade saved.", "success")
            return redirect(url_for("student_details", roll=roll))
        else:
            flash("Invalid input or student not found.", "danger")
            return redirect(url_for("add_grade"))
    students = tracker.list_students()
    subjects = tracker.get_subjects()
    return render_template("add_grade.html", students=students, subjects=subjects)

@app.route("/average/<roll>")
def average(roll):
    avg = tracker.calculate_average(roll)
    if avg is None:
        flash("Student not found or no grades.", "warning")
        return redirect(url_for("students"))
    flash(f"Average for {roll} is {avg:.2f}", "info")
    return redirect(url_for("student_details", roll=roll))

@app.route("/delete-student/<roll>", methods=["POST"])
def delete_student(roll):
    if tracker.delete_student(roll):
        flash(f"Student {roll} deleted successfully.", "success")
    else:
        flash("Student not found.", "danger")
    return redirect(url_for("students"))

@app.route("/add-subject", methods=["GET", "POST"])
def add_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Subject name is required.", "warning")
            return redirect(url_for("add_subject"))
        if tracker.add_subject(name):
            flash(f"Subject '{name}' added successfully.", "success")
            return redirect(url_for("index"))
        else:
            flash("Subject already exists.", "danger")
            return redirect(url_for("add_subject"))
    return render_template("add_subject.html")

# ---- optional bonus routes ----
@app.route("/report/topper/<subject>")
def topper(subject):
    res = tracker.subject_topper(subject)
    students = tracker.list_students()

    subjects = tracker.get_subjects()
    topper_results = {s: None for s in subjects}
    if res:
        topper_results[subject] = f"Topper in {subject}: {res['name']} ({res['roll_number']}) - {res['score']}"
    else:
        topper_results[subject] = f"No topper available for {subject} yet."

    return render_template("index.html",
                           students=students,
                           subjects=subjects,
                           topper_results=topper_results,
                           avg_results={s: None for s in subjects})


@app.route("/report/class-average/<subject>")
def class_avg(subject):
    avg = tracker.class_average_for_subject(subject)
    students = tracker.list_students()

    subjects = tracker.get_subjects()
    avg_results = {s: None for s in subjects}
    if avg is not None:
        avg_results[subject] = f"Class average in {subject}: {avg:.2f}"
    else:
        avg_results[subject] = f"No average available for {subject} yet."

    return render_template("index.html",
                           students=students,
                           subjects=subjects,
                           topper_results={s: None for s in subjects},
                           avg_results=avg_results)



if __name__ == "__main__":
    app.run(debug=True)
