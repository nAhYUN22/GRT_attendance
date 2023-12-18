document.addEventListener("DOMContentLoaded", function () {
    const meetingForm = document.getElementById("meeting_form");
    const meeting_submit = document.getElementById("meeting_submit");

    meeting_submit.addEventListener("click", (e) => {
        e.preventDefault();
        const meeting_num = meetingForm.meeting_num.value;
        var csrfToken = getCookie('csrftoken');
        console.log(csrfToken);
        fetch('/grt/checkattendance/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                meetingroom: meeting_num,
            }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                } else {
                    console.log(data.participants);
                    const participantlist = document.getElementById("participant-list");
                    participantlist.innerHTML = "";

                    const participants = data.participants;
                    if (participants.length === 0) {
                        participantlist.innerHTML = "참가자 없음";
                    } else {
                        const ul = document.createElement("ul");
                        participants.forEach(participant => {
                            const li = document.createElement("li");
                            li.textContent = participant.name;
                            ul.appendChild(li);
                        });
                        participantlist.appendChild(ul);
                    }
                }
            });
    });
});

// CSRF 토큰을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
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