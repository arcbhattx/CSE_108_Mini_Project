from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))

    # Relationships
    courses_taught = db.relationship("Course", back_populates="teacher_rel")  # for teachers
    enrollments = db.relationship("Enrollment", back_populates="student")  # for students

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    capacity = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.String(50))  

    enrollments = db.relationship("Enrollment", back_populates="course")
    teacher_rel = db.relationship("User", back_populates="courses_taught", foreign_keys=[teacher_id])

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    grade = db.Column(db.String(5), nullable=True)

    student = db.relationship("User", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
