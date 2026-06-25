
import sqlite3
from contextlib import contextmanager

sqlite_file_name = "school.db"

@contextmanager
def get_connection():
    connection = sqlite3.connect(sqlite_file_name)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()

def create_table():
    with get_connection() as connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            country TEXT NOT NULL,
            id_number INTEGER NOT NULL
        )''')
        
        connection.execute('''CREATE TABLE IF NOT EXISTS courses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            course_code TEXT UNIQUE NOT NULL,
            credits INTEGER NOT NULL,
            department TEXT NOT NULL
        )''')

        connection.execute('''CREATE TABLE IF NOT EXISTS teachers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course_id TEXT,
            email TEXT NOT NULL,
            country TEXT NOT NULL,
            id_number INTEGER NOT NULL,
            FOREIGN KEY(course_id) REFERENCES courses(course_code) ON DELETE SET NULL
        )''')

def add_student(name, age, email, country, id_number):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO students (name, age, email, country, id_number) VALUES (?, ?, ?, ?, ?)',
            (name, age, email, country, id_number)
        )

def get_students():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM students').fetchall()

def get_student_by_id(id):
    with get_connection() as connection:
        return connection.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

def update_student(id, name, age, email, country, id_number):
    with get_connection() as connection:
        connection.execute(
            'UPDATE students SET name=?, age=?, email=?, country=?, id_number=? WHERE id=?',
            (name, age, email, country, id_number, id)
        )

def add_course(title, course_code, credits, department):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO courses (title, course_code, credits, department) VALUES (?, ?, ?, ?)',
            (title, course_code, credits, department)
        )

def get_courses():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM courses').fetchall()

def get_course_by_id(id):
    with get_connection() as connection:
        return connection.execute('SELECT * FROM courses WHERE id = ?', (id,)).fetchone()

def update_course(id, title, course_code, credits, department):
    with get_connection() as connection:
        connection.execute(
            'UPDATE courses SET title=?, course_code=?, credits=?, department=? WHERE id=?',
            (title, course_code, credits, department, id)
        )

def add_teacher(name, course_id, email, country, id_number):
    with get_connection() as connection:
        connection.execute(
            'INSERT INTO teachers (name, course_id, email, country, id_number) VALUES (?, ?, ?, ?, ?)',
            (name, course_id, email, country, id_number)
        )

def get_teachers():
    with get_connection() as connection:
        return connection.execute('SELECT * FROM teachers').fetchall()

def get_teacher_by_id(id):
    with get_connection() as connection:
        return connection.execute('SELECT * FROM teachers WHERE id = ?', (id,)).fetchone()

def update_teacher(id, name, course_id, email, country, id_number):
    with get_connection() as connection:
        connection.execute(
            'UPDATE teachers SET name=?, course_id=?, email=?, country=?, id_number=? WHERE id=?',
            (name, course_id, email, country, id_number, id)
        )

def delete_record(table_name, id):
    allowed_tables = {"students", "courses", "teachers"}
    if table_name not in allowed_tables:
        raise ValueError(f"Unauthorized table access: {table_name}")
        
    with get_connection() as connection:
        connection.execute(f'DELETE FROM {table_name} WHERE id = ?', (id,))
