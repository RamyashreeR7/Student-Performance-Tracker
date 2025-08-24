# cli.py
from flask import Flask
from models import db
from tracker import StudentTracker
from config import DATABASE_URI

def init_db():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

def menu():
    tracker = StudentTracker()
    while True:
        print("\n--- Student Performance Tracker (CLI) ---")
        print("1. Add Student")
        print("2. Add/Update Grade")
        print("3. View Student Details")
        print("4. Calculate Student Average")
        print("5. List Students")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Name: ")
            roll = input("Roll Number: ")
            ok = tracker.add_student(name, roll)
            print("✔ Added." if ok else "✖ Roll number already exists.")
        elif choice == "2":
            roll = input("Roll Number: ")
            subject = input("Subject (Math/Science/English): ")
            try:
                score = float(input("Score (0-100): "))
            except ValueError:
                print("✖ Enter a valid number.")
                continue
            ok = tracker.add_grade(roll, subject, score)
            print("✔ Saved." if ok else "✖ Invalid input or student not found.")
        elif choice == "3":
            roll = input("Roll Number: ")
            w = tracker.view_student_details(roll)
            if not w:
                print("✖ Not found.")
            else:
                print(f"Name: {w.name} | Roll: {w.roll_number}")
                print("Grades:", w.grades_dict or "(none)")
                print("Average:", w.average())
        elif choice == "4":
            roll = input("Roll Number: ")
            avg = tracker.calculate_average(roll)
            print("Average:", avg if avg is not None else "✖ Not found or no grades.")
        elif choice == "5":
            for w in tracker.list_students():
                print(f"{w.roll_number} - {w.name} | Avg: {w.average()}")
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("✖ Invalid option.")

if __name__ == "__main__":
    app = init_db()
    with app.app_context():
        menu()
