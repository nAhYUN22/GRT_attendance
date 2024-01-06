// main.js

function sendRequest(page) {
    fetch(`/${page}/`)
        .then(response => response.text())
        .then(html => {
            document.open();
            document.write(html);
            document.close();
        })
        .catch(error => console.error('Error:', error));
}
