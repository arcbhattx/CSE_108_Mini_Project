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

const urlParams = new URLSearchParams(window.location.search);
const courseId = urlParams.get("course_id");

window.onload = () => {
    loadStudents();
};

async function loadStudents() {
    try {
        const res = await fetch(`${API}/teacher/class/${courseId}/students`, { headers: getHeaders() });
        if (!res.ok) throw await res.json();

        const data = await res.json();
        const tbody = document.getElementById("students");
        tbody.innerHTML = "";

        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="3">No students enrolled in this course.</td></tr>`;
            return;
        }

        data.forEach(s => {
            tbody.innerHTML += `
                <tr>
                    <td>${s.student_username}</td>
                    <td><input id="grade-${s.enrollment_id}" value="${s.grade ?? ""}" placeholder="Enter grade"></td>
                    <td><button onclick="updateGrade(${s.enrollment_id})">Update</button></td>
                </tr>
            `;
        });
    } catch (err) {
        alert(err.error || "Failed to load students.");
    }
}

function updateGrade(enrollmentId) {
    const newGrade = document.getElementById(`grade-${enrollmentId}`).value;

    fetch(`${API}/teacher/update-grade`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({ enrollment_id: enrollmentId, grade: newGrade })
    })
    .then(r => r.json())
    .then(data => {
        alert(data.message);
        loadStudents();
    });
}
function goBack() {
    window.location = "teacher.html";
}
