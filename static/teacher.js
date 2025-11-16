const API = "http://localhost:3000";

function getHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem("token")
    };
}

function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}

window.onload = () => {
    loadCourses();
};

function loadCourses() {
    fetch(`${API}/teacher/classes`, {
        headers: getHeaders()
    })
    .then(r => r.json())
    .then(async data => {
        const div = document.getElementById("courses");
        div.innerHTML = "";

        for (const c of data) {
        div.innerHTML += `
            <div class="card">
                <strong>${c.name}</strong><br>
                Teacher: ${c.teacher_name}<br>
                Time: ${c.time}<br>
                Enrolled: ${c.enrolled}/${c.capacity}<br><br>
                <button onclick="showStudents(${c.id})">View Students</button>
            </div>
        `;
    }

    });
}

function updateGrade(enrollmentId) {
    const newGrade = document.getElementById(`grade-${enrollmentId}`).value;

    fetch(`${API}/teacher/update-grade`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({
            enrollment_id: enrollmentId,
            grade: newGrade
        })
    })
    .then(r => r.json())
    .then(data => {
        alert(data.message);
    });
}

function showStudents(courseId) {
    fetch(`${API}/teacher/class/${courseId}/students`, {
        headers: getHeaders()
    })
    .then(r => r.json())
    .then(data => {
        const div = document.getElementById("students");
        div.innerHTML = "";

        if (data.length === 0) {
            div.innerHTML = "<p>No students enrolled in this course.</p>";
            return;
        }

        data.forEach(s => {
            div.innerHTML += `
                <div class="card">
                    <strong>${s.student_username}</strong><br>
                    Grade: ${s.grade ?? "N/A"}<br><br>
                    <input id="grade-${s.enrollment_id}" placeholder="Enter grade">
                    <button onclick="updateGrade(${s.enrollment_id})">Update Grade</button>
                </div>
            `;
        });
    });
}
