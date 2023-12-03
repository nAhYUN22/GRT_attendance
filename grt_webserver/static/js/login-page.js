const loginForm = document.getElementById("login-form");
const submitButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

submitButton.addEventListener("click", (event) => {
    event.preventDefault();
    const user_id = loginForm.user_id.value;
    const password = loginForm.password.value;

    console.log(user_id);

    fetch('/grt/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // 'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            ID: user_id,
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
            alert("You have successfully logged in. User: " + data.ID);
            // 필요한 경우, 토큰을 localStorage나 sessionStorage에 저장할 수 있습니다.
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('isLoggedIn', 'true');
            console.log(localStorage.getItem('authToken'));
            // fetch('/') // 메인 페이지 URL로 변경
            window.location.href = '/';
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

// CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}