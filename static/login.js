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

        // Save token in localStorage
        localStorage.setItem("token", data.token);

        // Decode JWT to check role
        const payload = JSON.parse(atob(data.token.split(".")[1]));

        // Redirect based on role
        if (payload.role === "student") {
            window.location.href = "/static/student.html";
        } else if (payload.role === "teacher") {
            window.location.href = "/static/teacher.html";
        } else if (payload.role === "admin") {
            window.location.href = "/admin";  // <-- go to Flask-Admin
        }
    });
}
