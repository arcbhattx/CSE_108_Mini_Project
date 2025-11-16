function login() {
    fetch("http://localhost:3000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert("Invalid credentials");
            return;
        }

        localStorage.setItem("token", data.token);

        // decode jwt
        const payload = JSON.parse(atob(data.token.split(".")[1]));

        // FIX: Add /static/ before the HTML file
        if (payload.role === "student") {
            window.location.href = "/static/student.html";
        } else if (payload.role === "teacher") {
            window.location.href = "/static/teacher.html";
        } else if (payload.role === "admin") {
            window.location.href = "/static/admin.html";  // Flask-Admin dashboard
        }

    });
}
