const API = "http://localhost:3000";

// Add Bearer prefix to token
function getHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

// Logout
function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}

// Check login on page load
window.onload = () => {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Not logged in!");
        window.location = "login.html";
        return;
    }

    loadMyCourses();
    loadAllCourses();
};

// Load my enrolled courses
// Load my enrolled courses
async function loadMyCourses() {
    try {
        const res = await fetch(`${API}/student/my-courses`, {
            headers: getHeaders()
        });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const div = document.getElementById("my-courses");
        div.innerHTML = "";

        if (data.length === 0) {
            div.innerHTML = "<p>You are not enrolled in any courses.</p>";
            return;
        }

        data.forEach(c => {
            div.innerHTML += `
                <div class="card">
                    <strong>${c.course_name}</strong><br>
                    Teacher: ${c.teacher_name}<br>
                    Time: ${c.time}<br>
                    Enrolled: ${c.enrolled}/${c.capacity}<br>
                    <button onclick="drop(${c.course_id})">Drop</button>
                </div>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load your courses.");
    }
}


// Load all courses
async function loadAllCourses() {
    try {
        const res = await fetch(`${API}/student/all-courses`, {
            headers: getHeaders()
        });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const div = document.getElementById("all-courses");
        div.innerHTML = "";

        // Fetch current student's courses to know which ones are enrolled
        const myCoursesRes = await fetch(`${API}/student/my-courses`, { headers: getHeaders() });
        const myCourses = await myCoursesRes.json();
        const enrolledCourseIds = myCourses.map(c => c.course_id);

        data.forEach(c => {
            const enrolled = enrolledCourseIds.includes(c.id);
            div.innerHTML += `
                <div class="card">
                    <strong>${c.name}</strong><br>
                    Teacher: ${c.teacher_name}<br>
                    Time: ${c.time}<br>
                    Enrolled: ${c.enrolled}/${c.capacity}<br><br>
                    ${enrolled
                        ? `<button onclick="drop(${c.id})">Drop</button>`
                        : `<button onclick="enroll(${c.id})" ${c.enrolled >= c.capacity ? "disabled" : ""}>
                             ${c.enrolled >= c.capacity ? "Full" : "Enroll"}
                           </button>`}
                </div>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load all courses.");
    }
}

// Enroll in a course
async function enroll(courseId) {
    try {
        const res = await fetch(`${API}/student/enroll`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({ course_id: courseId })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.message);
            loadMyCourses();
            loadAllCourses();
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert("Failed to enroll.");
    }
}

// Drop class
async function drop(courseId) {
    try {
        const res = await fetch(`${API}/student/drop/${courseId}`, {
            method: "DELETE",
            headers: getHeaders()
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.message);
            loadMyCourses();
            loadAllCourses();
        } else {
            alert(data.error);
        }
    } catch (err) {
        alert("Failed to drop class.");
    }
}
