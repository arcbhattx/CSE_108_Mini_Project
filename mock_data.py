from app import app
from models import db, User, Course
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # ---- USERS ----
    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        role="admin"
    )
    
    teacher = User(
        username="teacher1",
        password=generate_password_hash("teach123"),
        role="teacher"
    )

    student1 = User(
        username="student1",
        password=generate_password_hash("stud123"),
        role="student"
    )

    student2 = User(
        username="student2",
        password=generate_password_hash("stud123"),
        role="student"
    )

    # ---- COURSES ----
    c1 = Course(name="CSE 101", capacity=30, teacher_id=2)
    c2 = Course(name="CSE 162", capacity=25, teacher_id=2)
    c3 = Course(name="MATH 221", capacity=40, teacher_id=2)

    db.session.add_all([admin, teacher, student1, student2, c1, c2, c3])
    db.session.commit()

    print("Database seeded successfully!")
