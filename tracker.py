# tracker.py
from typing import Optional, Dict, List
from statistics import mean
from models import db, Student, Grade, Subject

# --- OOP API ---

class StudentWrapper:
    """In-memory view over DB row; includes grade helpers."""
    def __init__(self, row: Student):
        self.name = row.name
        self.roll_number = row.roll_number
        self.grades_dict: Dict[str, float] = {g.subject: g.score for g in row.grades}

    def add_grade(self, subject: str, score: float):
        self.grades_dict[subject] = score

    def average(self) -> Optional[float]:
        return mean(self.grades_dict.values()) if self.grades_dict else None

    def info(self) -> Dict:
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "grades": self.grades_dict,
            "average": self.average()
        }

class StudentTracker:
    """Manages students + grades, backed by SQLAlchemy (SQLite)."""

    # ---- helpers ----
    def _get_student_row(self, roll_number: str) -> Optional[Student]:
        return Student.query.filter_by(roll_number=roll_number).first()

    def roll_is_unique(self, roll_number: str) -> bool:
        return self._get_student_row(roll_number) is None

    # ---- core ----
    def add_student(self, name: str, roll_number: str) -> bool:
        if not self.roll_is_unique(roll_number):
            return False
        s = Student(name=name.strip(), roll_number=roll_number.strip())
        db.session.add(s)
        db.session.commit()
        return True

    def add_grade(self, roll_number: str, subject: str, score: float) -> bool:
        row = self._get_student_row(roll_number)
        if row is None:
            return False
        if not (0 <= score <= 100):
            return False
        # Upsert subject grade
        g = next((gr for gr in row.grades if gr.subject == subject), None)
        if g:
            g.score = score
        else:
            db.session.add(Grade(subject=subject, score=score, student=row))
        db.session.commit()
        return True

    def view_student_details(self, roll_number: str) -> Optional[StudentWrapper]:
        row = self._get_student_row(roll_number)
        return StudentWrapper(row) if row else None

    def calculate_average(self, roll_number: str) -> Optional[float]:
        w = self.view_student_details(roll_number)
        return w.average() if w else None

    # ---- reports (bonus-friendly but optional) ----
    def subject_topper(self, subject: str) -> Optional[Dict]:
        q = (Grade.query.filter_by(subject=subject)
                        .order_by(Grade.score.desc())
                        .first())
        if not q:
            return None
        stud = Student.query.get(q.student_id)
        return {"roll_number": stud.roll_number, "name": stud.name, "score": q.score}

    def class_average_for_subject(self, subject: str) -> Optional[float]:
        grades: List[Grade] = Grade.query.filter_by(subject=subject).all()
        return mean([g.score for g in grades]) if grades else None

    def list_students(self) -> List[StudentWrapper]:
        return [StudentWrapper(s) for s in Student.query.order_by(Student.roll_number).all()]

    def delete_student(self, roll_number: str) -> bool:
        """Delete a student and all associated grades."""
        row = self._get_student_row(roll_number)
        if row is None:
            return False
        db.session.delete(row)
        db.session.commit()
        return True

    # ---- subject management ----
    def add_subject(self, name: str) -> bool:
        """Add a new subject."""
        name = name.strip()
        if not name:
            return False
        if Subject.query.filter_by(name=name).first():
            return False  # Subject already exists
        subject = Subject(name=name)
        db.session.add(subject)
        db.session.commit()
        return True

    def get_subjects(self) -> List[str]:
        """Get all available subjects."""
        subjects = Subject.query.order_by(Subject.name).all()
        return [s.name for s in subjects]

    def delete_subject(self, name: str) -> bool:
        """Delete a subject and all associated grades."""
        subject = Subject.query.filter_by(name=name).first()
        if not subject:
            return False
        # Delete all grades for this subject
        Grade.query.filter_by(subject=name).delete()
        db.session.delete(subject)
        db.session.commit()
        return True
