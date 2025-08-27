# Student Performance Tracker

## Project Title
**Student Performance Tracker**

---

## Project Description
The Student Performance Tracker is a Python-based application that helps teachers manage and analyze student grades.  

The project started as a simple console (CLI) program to practice **Python fundamentals, loops, conditionals, and OOP**. It was later extended into a full **Flask web application** with database integration so that teachers can easily interact with the system through a browser.  

### Key Features
- Add new students with unique roll numbers
- Assign or update grades for subjects (Math, Science, English by default)
- View individual student details with their grades
- Calculate average grade per student
- Store data persistently with SQLite (or PostgreSQL when deployed)
- Simple, user-friendly web interface built with Flask and HTML templates

**Bonus Features:**
- Find the topper in a particular subject
- View the class average for a subject
- CLI version available for quick testing and practice

---

## Technologies Used
- **Programming Language:** Python 3  
- **Web Framework:** Flask  
- **Database:** SQLite (default), PostgreSQL (for deployment)  
- **ORM:** SQLAlchemy, Flask-SQLAlchemy  
- **Deployment:** Gunicorn + Procfile (Heroku/Render/Railway ready)  
- **Frontend:** HTML (Jinja templates), CSS (SimpleCSS)  

---

## Requirements
Before running this project, make sure you have:
- Python 3.8 or higher  
- `pip` (Python package manager)  
- A virtual environment (recommended)  
- The packages listed in `requirements.txt`  

---

## Installation Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RamyashreeR7/student-performance-tracker.git
   cd student-performance-tracker
