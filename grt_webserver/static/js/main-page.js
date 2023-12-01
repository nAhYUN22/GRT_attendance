
document.addEventListener("DOMContentLoaded", () => {
    // 페이지 로드 시 로그인 상태 확인
    checkLoginStatus();
});

const loginButton = document.getElementById("loginButton");
const studentInfoButton = document.getElementById("studentInfoButton");
const attendanceCheckButton = document.getElementById("attendanceCheckButton");

loginButton.addEventListener("click", loginHandler);

function loginHandler(event) {
    fetch('/grt/login/', { method: 'GET' })
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html;
        });
}

function logoutHandler(event) {
    // 로그아웃 처리 로직을 여기에 추가합니다.
    alert("Logged out successfully!");
    // 로그아웃 후 필요한 UI 업데이트나 페이지 리디렉션 처리
}


studentInfoButton.addEventListener("click", function () {
    fetch('/student-info/', { method: 'GET' })
        .then(response => response.text())
        .then(html => document.body.innerHTML = html);
});

attendanceCheckButton.addEventListener("click", function () {
    fetch('/attendance-check/', { method: 'GET' })
        .then(response => response.text())
        .then(html => document.body.innerHTML = html);
});

function checkLoginStatus() {
    // 예: localStorage에서 로그인 상태 확인
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const authToken = localStorage.getItem('authToken');
    console.log(isLoggedIn);
    console.log(authToken);
    fetch('/grt/auth/check_login/', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                // 사용자가 로그인한 경우
                console.log('사용자가 로그인되어 있습니다.');
                loginButton.textContent = "Logout";
                loginButton.removeEventListener("click", loginHandler);
                loginButton.addEventListener("click", logoutHandler);

            }
        })
        .catch(error => {
            console.error('로그인 상태 확인 오류:', error);
        });

}