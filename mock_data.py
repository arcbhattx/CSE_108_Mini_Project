from app import app
from models import db, User, Course
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

   
    admin = User(
        username="admin",
        password=generate_password_hash("admin123"),
        role="admin"
    )
    
    teacher1 = User(
        username="teacher1",
        password=generate_password_hash("teach123"),
        role="teacher"
    )

    teacher2 = User(
        username="teacher2",
        password=generate_password_hash("teach456"),
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

    student3 = User(
        username="student3",
        password=generate_password_hash("stud123"),
        role="student"
    )

    db.session.add_all([admin, teacher1, teacher2, student1, student2, student3])
    db.session.commit()

 
    c1 = Course(name="CSE 101", capacity=30, teacher_id=teacher1.id, time="MWF 9:00-9:50 AM")
    c2 = Course(name="CSE 162", capacity=25, teacher_id=teacher1.id, time="TR 11:00-11:50 AM")

    c3 = Course(name="MATH 221", capacity=40, teacher_id=teacher2.id, time="MWF 10:00-10:50 AM")
    c4 = Course(name="PHY 101", capacity=35, teacher_id=teacher2.id, time="TR 2:00-2:50 PM")

    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    print("Database seeded successfully!")
    print(f"Admin -> username: admin | password: admin123")
    print(f"Teacher1 -> username: teacher1 | password: teach123")
    print(f"Teacher2 -> username: teacher2 | password: teach456")
    print(f"Student1 -> username: student1 | password: stud123")
    print(f"Student2 -> username: student2 | password: stud123")
    print(f"Student3 -> username: student3 | password: stud123")
