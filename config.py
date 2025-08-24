# config.py
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'students.db')}")
