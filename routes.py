# routes.py
from flask import Blueprint, request, jsonify
from models import db, User, Course, Enrollment
from auth import auth_required, generate_token
from werkzeug.security import check_password_hash

routes = Blueprint("routes", __name__)



#  AUTH ROUTES

@routes.post("/login")
def login():
    data = request.json
    
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)
    return jsonify({"token": token})


@routes.post("/logout")
@auth_required()
def logout():
    # Token authentication = logout happens on frontend (delete token)
    return jsonify({"message": "Logged out"})


#  STUDENT ROUTES

@routes.get("/student/all-courses")
@auth_required("student")
def all_courses():
    courses = Course.query.all()
    result = []

    for c in courses:
        enrolled_count = Enrollment.query.filter_by(course_id=c.id).count()
        result.append({
            "id": c.id,
            "name": c.name,
            "capacity": c.capacity,
            "teacher_name": c.teacher_rel.username if c.teacher_rel else "TBD",
            "time": c.time,
            "enrolled": enrolled_count
        })
    return jsonify(result)


# Drop a course
@routes.delete("/student/drop/<int:course_id>")
@auth_required("student")
def drop_class(course_id):
    sid = request.user["id"]
    enrollment = Enrollment.query.filter_by(student_id=sid, course_id=course_id).first()
    if not enrollment:
        return jsonify({"error": "Not enrolled in this course"}), 400

    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Class dropped successfully"})




@routes.get("/student/my-courses")
@auth_required("student")
def my_courses():
    sid = request.user["id"]

    enrolls = (
        Enrollment.query
        .filter_by(student_id=sid)
        .join(Course, Enrollment.course_id == Course.id)
        .join(User, Course.teacher_id == User.id)  # join teacher
        .add_entity(Course)
        .add_entity(User)
    )

    result = []
    for e in enrolls:
        enrollment_obj = e[0]  # Enrollment
        course_obj = e[1]      # Course
        teacher_obj = e[2]     # User (teacher)

        enrolled_count = Enrollment.query.filter_by(course_id=course_obj.id).count()

        result.append({
            "course_id": course_obj.id,
            "course_name": course_obj.name,
            "teacher_name": teacher_obj.username if teacher_obj else "TBD",
            "time": course_obj.time,
            "enrolled": enrolled_count,
            "capacity": course_obj.capacity,
            "grade": enrollment_obj.grade
        })

    return jsonify(result)



@routes.get("/student/class/<int:course_id>/count")
@auth_required("student")
def class_count(course_id):
    count = Enrollment.query.filter_by(course_id=course_id).count()
    return jsonify({"course_id": course_id, "count": count})


@routes.post("/student/enroll")
@auth_required("student")
def enroll():
    data = request.json
    sid = request.user["id"]
    cid = data["course_id"]

    course = Course.query.get(cid)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    count = Enrollment.query.filter_by(course_id=cid).count()
    if count >= course.capacity:
        return jsonify({"error": "Class is full"}), 400

    if Enrollment.query.filter_by(student_id=sid, course_id=cid).first():
        return jsonify({"error": "Already enrolled"}), 400

    new_enroll = Enrollment(student_id=sid, course_id=cid)
    db.session.add(new_enroll)
    db.session.commit()
    return jsonify({"message": "Enrolled successfully"})

# 👨‍🏫 TEACHER ROUTE

@routes.get("/teacher/classes")
@auth_required("teacher")
def teacher_classes():
    tid = request.user["id"]
    courses = Course.query.filter_by(teacher_id=tid).all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "capacity": c.capacity
        }
        for c in courses
    ])


@routes.get("/teacher/class/<int:course_id>/students")
@auth_required("teacher")
def teacher_class_students(course_id):
    tid = request.user["id"]

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    if course.teacher_id != tid:
        return jsonify({"error": "Forbidden"}), 403

    enrolls = (
        Enrollment.query
        .filter_by(course_id=course_id)
        .join(User, Enrollment.student_id == User.id)
    )

    return jsonify([
        {
            "enrollment_id": e.id,
            "student_id": e.student_id,
            "student_username": e.student.username,
            "grade": e.grade
        }
        for e in enrolls
    ])


@routes.post("/teacher/update-grade")
@auth_required("teacher")
def update_grade():
    data = request.json
    enrollment_id = data["enrollment_id"]
    new_grade = data["grade"]

    enr = Enrollment.query.get(enrollment_id)
    if not enr:
        return jsonify({"error": "Enrollment not found"}), 404

    # verify teacher owns the class
    course = Course.query.get(enr.course_id)
    if course.teacher_id != request.user["id"]:
        return jsonify({"error": "Forbidden"}), 403

    enr.grade = new_grade
    db.session.commit()

    return jsonify({"message": "Grade updated"})


