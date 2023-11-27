const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginButton.addEventListener("click", (event) => {
    event.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    fetch('/grt/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ID: username,
            password: password
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert("You have successfully logged in.")
            } else {
                loginErrorMsg.textContent = "Error: Invalid login credentials";
                loginErrorMsg.style.opacity = 1;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
