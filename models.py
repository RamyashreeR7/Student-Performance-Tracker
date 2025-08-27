# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    grades = db.relationship("Grade", backref="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Student {self.roll_number} - {self.name}>"

class Subject(db.Model):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"<Subject {self.name}>"

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(64), nullable=False)
    score = db.Column(db.Float, nullable=False)  # 0..100
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    def __repr__(self):
        return f"<Grade {self.subject}: {self.score}>"
