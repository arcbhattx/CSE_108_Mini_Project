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

async function loadCourses() {
    try {
        const res = await fetch(`${API}/teacher/classes`, { headers: getHeaders() });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const tbody = document.getElementById("courses");
        tbody.innerHTML = "";

        data.forEach(c => {
            tbody.innerHTML += `
                <tr>
                    <td><a href="course.html?course_id=${c.id}">${c.name}</a></td>
                    <td>${c.teacher_name}</td>
                    <td>${c.time}</td>
                    <td>${c.enrolled}/${c.capacity}</td>
                </tr>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load courses.");
    }
}
