const meeting_num = document.getElementById("meeting_num");
const meeting_submit = document.getElementById("meeting_submit");

meeting_submit.addEventListener("click", (e) => {
    const meetingroom = meeting_num.value;
    fetch('/grt/checkattendance/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            // 'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            meetingroom: meetingroom,
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