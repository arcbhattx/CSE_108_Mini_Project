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
            "teacher_id": c.teacher_id,
            "enrolled": enrolled_count
        })

    return jsonify(result)


@routes.get("/student/my-courses")
@auth_required("student")
def my_courses():
    sid = request.user["id"]

    enrolls = (
        Enrollment.query
        .filter_by(student_id=sid)
        .join(Course, Enrollment.course_id == Course.id)
    )

    return jsonify([
        {
            "course_id": e.course_id,
            "course_name": e.course.name,
            "grade": e.grade
        }
        for e in enrolls
    ])


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

    # check capacity
    count = Enrollment.query.filter_by(course_id=cid).count()
    if count >= course.capacity:
        return jsonify({"error": "Class is full"}), 400

    # prevent duplicate enrollment
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


# ADMIN 

# ----------------------
# ADMIN ROUTES
# ----------------------
from auth import auth_required  # make sure this is already imported

# --- USERS ---
@routes.get("/admin/users")
@auth_required("admin")
def admin_get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "role": u.role} for u in users])


@routes.post("/admin/users")
@auth_required("admin")
def admin_create_user():
    data = request.json
    if not all(k in data for k in ("username", "password", "role")):
        return jsonify({"error": "Missing fields"}), 400

    new_user = User(
        username=data["username"],
        password=data["password"],  # consider hashing in production
        role=data["role"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


@routes.delete("/admin/users/<int:user_id>")
@auth_required("admin")
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})


# --- COURSES ---
@routes.get("/admin/courses")
@auth_required("admin")
def admin_get_courses():
    courses = Course.query.all()
    return jsonify([
        {"id": c.id, "name": c.name, "capacity": c.capacity, "teacher_id": c.teacher_id} 
        for c in courses
    ])


@routes.post("/admin/courses")
@auth_required("admin")
def admin_create_course():
    data = request.json
    if not all(k in data for k in ("name", "capacity", "teacher_id")):
        return jsonify({"error": "Missing fields"}), 400

    new_course = Course(
        name=data["name"],
        capacity=data["capacity"],
        teacher_id=data["teacher_id"]
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"message": "Course created"}), 201


@routes.delete("/admin/courses/<int:course_id>")
@auth_required("admin")
def admin_delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted"})


# --- ENROLLMENTS ---
@routes.get("/admin/enrollments")
@auth_required("admin")
def admin_get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify([
        {
            "id": e.id,
            "student_id": e.student_id,
            "course_id": e.course_id,
            "grade": e.grade
        }
        for e in enrollments
    ])


@routes.delete("/admin/enrollments/<int:enrollment_id>")
@auth_required("admin")
def admin_delete_enrollment(enrollment_id):
    enr = Enrollment.query.get(enrollment_id)
    if not enr:
        return jsonify({"error": "Enrollment not found"}), 404

    db.session.delete(enr)
    db.session.commit()
    return jsonify({"message": "Enrollment deleted"})
