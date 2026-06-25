from fastapi import FastAPI
from pydantic import BaseModel
from database import *

app = FastAPI()

create_table()


class Student(BaseModel):
    name: str
    age: int
    email: str
    country: str
    id_number: int

class Course(BaseModel):
    title: str
    course_code: str
    credits: int
    department: str

class Teacher(BaseModel):
    name: str
    course_id: str | None = None
    email: str
    country: str
    id_number: int


@app.get("/")
def home():
    return {"message": "Welcome to my API Server"}


@app.post("/students")
def register_student(student: Student):
    add_student(student.name, student.age, student.email, student.country, student.id_number)
    return {"message": "User registered successfully!", "student": student}

@app.get("/students")
def get_all_students():
    students = get_students()
    return students

@app.get("/students/{id}")
def student_details(id: int):
    student = get_student_by_id(id)
    return student

@app.put("/students/{id}")
def edit_student(id: int, student: Student):
    update_student(id, student.name, student.age, student.email, student.country, student.id_number)
    return {"message": "Student updated successfully"}

@app.delete("/students/{id}")
def remove_student(id: int):
    delete_record("students", id)
    return {"message": "Student deleted successfully"}



@app.post("/courses")
def register_course(course: Course):
    add_course(course.title, course.course_code, course.credits, course.department)
    return {"message": "Course created successfully!", "course": course}

@app.get("/courses")
def get_all_courses():
    courses = get_courses()
    return courses

@app.get("/courses/{id}")
def course_details(id: int):
    course = get_course_by_id(id)
    return course

@app.put("/courses/{id}")
def edit_course(id: int, course: Course):
    update_course(id, course.title, course.course_code, course.credits, course.department)
    return {"message": "Course updated successfully"}

@app.delete("/courses/{id}")
def remove_course(id: int):
    delete_record("courses", id)
    return {"message": "Course deleted successfully"}


@app.post("/teachers")
def register_teacher(teacher: Teacher):
    add_teacher(teacher.name, teacher.course_id, teacher.email, teacher.country, teacher.id_number)
    return {"message": "Teacher registered successfully!", "teacher": teacher}

@app.get("/teachers")
def get_all_teachers():
    teachers = get_teachers()
    return teachers

@app.get("/teachers/{id}")
def teacher_details(id: int):
    teacher = get_teacher_by_id(id)
    return teacher

@app.put("/teachers/{id}")
def edit_teacher(id: int, teacher: Teacher):
    update_teacher(id, teacher.name, teacher.course_id, teacher.email, teacher.country, teacher.id_number)
    return {"message": "Teacher updated successfully"}

@app.delete("/teachers/{id}")
def remove_teacher(id: int):
    delete_record("teachers", id)
    return {"message": "Teacher deleted successfully"}
