const API = "http://localhost:3000";


function getHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}


function logout() {
    localStorage.removeItem("token");
    window.location = "login.html";
}

function openTab(tabName, element) {
    document.querySelectorAll(".tabcontent").forEach(t => t.style.display = "none");
    document.getElementById(tabName).style.display = "block";

    document.querySelectorAll(".tablink").forEach(b => b.classList.remove("active"));
    element.classList.add("active");
}


window.onload = () => {
    const username = localStorage.getItem("username");
    if (!username) {
        alert("Not logged in!");
        window.location = "login.html";
        return;
    }

    document.getElementById("welcome").textContent = `Welcome, ${username}`;

    loadMyCourses();
    loadAllCourses();
};



async function loadMyCourses() {
    try {
        const res = await fetch(`${API}/student/my-courses`, { headers: getHeaders() });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const tbody = document.getElementById("my-courses");
        tbody.innerHTML = "";

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6">You are not enrolled in any courses.</td></tr>`;
            return;
        }

        data.forEach(c => {
            tbody.innerHTML += `
                <tr>
                    <td>${c.course_name}</td>
                    <td>${c.teacher_name}</td>
                    <td>${c.time}</td>
                    <td>${c.enrolled}/${c.capacity}</td>
                    <td>${c.grade ?? "N/A"}</td>
                    <td><button onclick="drop(${c.course_id})">Drop</button></td>
                </tr>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load your courses.");
    }
}


async function loadAllCourses() {
    try {
        const res = await fetch(`${API}/student/all-courses`, { headers: getHeaders() });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const tbody = document.getElementById("all-courses");
        tbody.innerHTML = "";

        const myCoursesRes = await fetch(`${API}/student/my-courses`, { headers: getHeaders() });
        const myCourses = await myCoursesRes.json();
        const enrolledCourseIds = myCourses.map(c => c.course_id);

        data.forEach(c => {
            const enrolled = enrolledCourseIds.includes(c.id);
            tbody.innerHTML += `
                <tr>
                    <td>${c.name}</td>
                    <td>${c.teacher_name}</td>
                    <td>${c.time}</td>
                    <td>${c.enrolled}/${c.capacity}</td>
                    <td>
                        ${enrolled
                            ? `<button onclick="drop(${c.id})">Drop</button>`
                            : `<button onclick="enroll(${c.id})" ${c.enrolled >= c.capacity ? "disabled" : ""}>
                                 ${c.enrolled >= c.capacity ? "Full" : "Enroll"}
                               </button>`}
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load all courses.");
    }
}


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
        } else alert(data.error);
    } catch (err) {
        alert("Failed to enroll.");
    }
}


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
        } else alert(data.error);
    } catch (err) {
        alert("Failed to drop class.");
    }
}
