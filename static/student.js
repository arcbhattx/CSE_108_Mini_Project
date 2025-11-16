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
    loadMyCourses();
    loadAllCourses();
};

function loadMyCourses() {
    fetch(`${API}/student/my-courses`, {
        headers: getHeaders()
    })
    .then(r => r.json())
    .then(data => {
        const div = document.getElementById("my-courses");
        div.innerHTML = "";
        data.forEach(c => {
            div.innerHTML += `
                <div class="card">
                    <strong>${c.course_name}</strong><br>
                    Grade: ${c.grade ?? "N/A"}
                </div>
            `;
        });
    });
}

function loadAllCourses() {
    fetch(`${API}/student/all-courses`, {
        headers: getHeaders()
    })
    .then(r => r.json())
    .then(data => {
        const div = document.getElementById("all-courses");
        div.innerHTML = "";
        data.forEach(c => {
            div.innerHTML += `
                <div class="card">
                    <strong>${c.name}</strong> <br>
                    Enrolled: ${c.enrolled}/${c.capacity}
                    <br><br>
                    <button class="enroll-btn" onclick="enroll(${c.id})">Enroll</button>
                </div>
            `;
        });
    });
}

function enroll(courseId) {
    fetch(`${API}/student/enroll`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({course_id: courseId})
    })
    .then(r => r.json())
    .then(data => {
        alert(data.message || data.error);
        loadMyCourses();
        loadAllCourses();
    });
}
