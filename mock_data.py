from app import app
from models import db, User, Course
from werkzeug.security import generate_password_hash

with app.app_context():
    # Drop and recreate tables
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

    # Add users to session first to get IDs
    db.session.add_all([admin, teacher, student1, student2])
    db.session.commit()

    # ---- COURSES ----
    # Assign teacher_id dynamically from the teacher object
    c1 = Course(name="CSE 101", capacity=30, teacher_id=teacher.id, time="MWF 9:00-9:50 AM")
    c2 = Course(name="CSE 162", capacity=25, teacher_id=teacher.id, time="TR 11:00-11:50 AM")
    c3 = Course(name="MATH 221", capacity=40, teacher_id=teacher.id, time="MWF 10:00-10:50 AM")

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Admin -> username: admin | password: admin123")
    print(f"Teacher -> username: teacher1 | password: teach123")
    print(f"Student1 -> username: student1 | password: stud123")
    print(f"Student2 -> username: student2 | password: stud123")
