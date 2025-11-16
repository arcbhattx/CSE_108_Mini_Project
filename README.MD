# ACME University Course Management System

This is a simple web-based course management system for students and teachers. Students can enroll in or drop courses, and teachers can view their classes and update student grades. An admin can manage all data through the Flask-Admin panel.

## Features

- **Student**
  - View enrolled courses
  - Enroll in available courses
  - Drop courses
- **Teacher**
  - View courses they teach
  - View students in each course
  - Update student grades
- **Admin**
  - Full CRUD access to all users, courses, and enrollments via Flask-Admin
- **Authentication**
  - JWT-based login system
  - Role-based routing for student, teacher, and admin dashboards

## Technologies Used

- **Backend**
  - Python 3.x
  - Flask (web framework)
  - Flask-SQLAlchemy (ORM for database)
  - Flask-JWT-Extended (JWT authentication)
  - Werkzeug (password hashing)
  
- **Frontend**
  - HTML / CSS / JavaScript
  - Vanilla JS for API calls and DOM manipulation
  - Fetch API for making requests to backend
  - Custom CSS for styling and responsive layout

- **Database**
  - SQLite (default with Flask-SQLAlchemy, stored locally)

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Seed the database**  
   To create initial users (admin, teachers, students) and courses:
   ```bash
   python mock_data.py
   ```
   > Note: This will drop and recreate all tables, so only run on a fresh setup or for testing.

4. **Run the backend**
   ```bash
   python app.py
   ```
   This will start the Flask backend at:  
   ```
   http://localhost:3000
   ```

5. **Open the frontend**  
   Open your browser and navigate to:  
   ```
   http://localhost:3000/static/login.html
   ```

## Login Credentials

**Admin**
- Username: `admin`
- Password: `admin123`

**Teachers**
- Username: `teacher1` | Password: `teach123`
- Username: `teacher2` | Password: `teach456`

**Students**
- Username: `student1` | Password: `stud123`
- Username: `student2` | Password: `stud123`
- Username: `student3` | Password: `stud123`

## File Structure

```
/project-root
│
├─ app.py                # Flask application entry point
├─ models.py             # Database models (User, Course, Enrollment)
├─ mock_data.py          # Script to feed the database
├─ auth.py               # authentication stuff
├─ routes.py               # authentication stuff
├─ requirements.txt      # Python dependencies

│
├─ /static
│   ├─ login.html        # Login page
│   ├─ student.html      # Student dashboard
│   ├─ teacher.html      # Teacher dashboard
│   ├─ student.js        # Student page JS
│   ├─ teacher.js        # Teacher page JS
│   ├─ login.js          # Login page JS
│   ├─ student.css       # Student page CSS
│   ├─ teacher.css       # Teacher page CSS
│   └─ login.css         # Login page CSS
│
└─ /templates            # Optional Flask templates if needed
```

## Notes

- The frontend is served via `/static` directory. No separate frontend server is required.
- JWT tokens are stored in `localStorage` for session persistence.
- Role-based routing ensures students, teachers, and admins only see authorized content.
- All changes (enrollments, grades, etc.) are persisted in the SQLite database.

