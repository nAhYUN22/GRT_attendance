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
        .then(response => {
            console.log(response)
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(err => { throw err; });
            }
        })
        .then(data => {
            // 성공적으로 로그인 되었다는 알림과 함께 토큰 처리
            console.log(data);
            alert("You have successfully logged in. Token: " + data.token);
            // 필요한 경우, 토큰을 localStorage나 sessionStorage에 저장할 수 있습니다.
            // 예: localStorage.setItem('token', data.token);
        })
        .catch((error) => {
            console.error('Error:', error);
            if (error.message) {
                loginErrorMsg.textContent = error.message;
            } else {
                loginErrorMsg.textContent = "Error: Invalid login credentials";
            }
            loginErrorMsg.style.opacity = 1;
        });
});
