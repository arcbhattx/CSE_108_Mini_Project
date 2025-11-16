const API_URL = "http://127.0.0.1:3000";  // your Flask backend
const token = localStorage.getItem("adminToken"); // store admin token after login

// TAB SWITCHING
function showSection(section) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById(`${section}-section`).style.display = 'block';
}

// FETCH USERS
async function fetchUsers() {
    const res = await fetch(`${API_URL}/admin/users`, {
    headers: { "Authorization": `Bearer ${token}` }
    });

    const users = await res.json();
    const usersList = document.getElementById("users-list");
    usersList.innerHTML = '';
    users.forEach(u => {
        const div = document.createElement('div');
        div.className = 'card';
        div.innerHTML = `
            <b>ID:</b> ${u.id} | <b>Username:</b> ${u.username} | <b>Role:</b> ${u.role}
            <button onclick="deleteUser(${u.id})">Delete</button>
        `;
        usersList.appendChild(div);
    });
}


async function createUser() {
    const username = document.getElementById("new-username").value;
    const password = document.getElementById("new-password").value;
    const role = document.getElementById("new-role").value;

    const res = await fetch(`${API_URL}/admin/users`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": token
        },
        body: JSON.stringify({ username, password, role })
    });

    if (res.ok) {
        alert("User created!");
        fetchUsers();
    } else {
        const err = await res.json();
        alert(err.error || "Failed to create user");
    }
}


async function deleteUser(id) {
    if(!confirm("Delete user?")) return;
    const res = await fetch(`${API_URL}/admin/users/${id}`, {
        method: "DELETE",
        headers: { "Authorization": token }
    });
    if (res.ok) {
        fetchUsers();
    } else {
        alert("Failed to delete user");
    }
}


async function fetchCourses() {
    const res = await fetch(`${API_URL}/admin/courses`, {
        headers: { "Authorization": token }
    });
    const courses = await res.json();
    const coursesList = document.getElementById("courses-list");
    coursesList.innerHTML = '';
    courses.forEach(c => {
        const div = document.createElement('div');
        div.className = 'card';
        div.innerHTML = `
            <b>ID:</b> ${c.id} | <b>Name:</b> ${c.name} | <b>Capacity:</b> ${c.capacity} | <b>Teacher ID:</b> ${c.teacher_id}
            <button onclick="deleteCourse(${c.id})">Delete</button>
        `;
        coursesList.appendChild(div);
    });
}


async function createCourse() {
    const name = document.getElementById("new-course-name").value;
    const capacity = parseInt(document.getElementById("new-course-capacity").value);
    const teacher_id = parseInt(document.getElementById("new-course-teacher-id").value);

    const res = await fetch(`${API_URL}/admin/courses`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": token
        },
        body: JSON.stringify({ name, capacity, teacher_id })
    });

    if (res.ok) {
        alert("Course created!");
        fetchCourses();
    } else {
        const err = await res.json();
        alert(err.error || "Failed to create course");
    }
}


async function deleteCourse(id) {
    if(!confirm("Delete course?")) return;
    const res = await fetch(`${API_URL}/admin/courses/${id}`, {
        method: "DELETE",
        headers: { "Authorization": token }
    });
    if (res.ok) {
        fetchCourses();
    } else {
        alert("Failed to delete course");
    }
}

async function fetchEnrollments() {
    const res = await fetch(`${API_URL}/admin/enrollments`, {
        headers: { "Authorization": token }
    });
    const enrollments = await res.json();
    const enrollmentsList = document.getElementById("enrollments-list");
    enrollmentsList.innerHTML = '';
    enrollments.forEach(e => {
        const div = document.createElement('div');
        div.className = 'card';
        div.innerHTML = `
            <b>ID:</b> ${e.id} | <b>Student ID:</b> ${e.student_id} | <b>Course ID:</b> ${e.course_id} | <b>Grade:</b> ${e.grade || "-"}
            <button onclick="deleteEnrollment(${e.id})">Delete</button>
        `;
        enrollmentsList.appendChild(div);
    });
}


async function deleteEnrollment(id) {
    if(!confirm("Delete enrollment?")) return;
    const res = await fetch(`${API_URL}/admin/enrollments/${id}`, {
        method: "DELETE",
        headers: { "Authorization": token }
    });
    if (res.ok) {
        fetchEnrollments();
    } else {
        alert("Failed to delete enrollment");
    }
}


showSection('users');
fetchUsers();
fetchCourses();
fetchEnrollments();
