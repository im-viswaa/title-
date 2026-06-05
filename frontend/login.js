function login() {

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (username === "") {
        alert("Enter Username");
        return;
    }

    if (password === "") {
        alert("Enter Password");
        return;
    }

    // Demo Login
    if (username === "admin" && password === "1234") {

        localStorage.setItem("loggedIn", "true");
        localStorage.setItem("username", username);

        alert("Login Successful");

        window.location.href = "dashboard.html";

    } else {

        alert("Invalid Username or Password");

    }
}

function checkLogin() {

    if (localStorage.getItem("loggedIn") !== "true") {

        window.location.href = "index.html";

    }
}

function logout() {

    localStorage.removeItem("loggedIn");
    localStorage.removeItem("username");

    alert("Logged Out");

    window.location.href = "index.html";
}