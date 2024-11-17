document.getElementById('authForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.getElementById('user').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        window.location.href = "/";
    } else {
        document.getElementById('errorPopup').style.display = "block";
    }
});

// Закрытие окна по клику за его пределами
window.onclick = function(event) {
    const popup = document.getElementById('errorPopup');
    const popupContent = document.querySelector('.popup-content');
    if (event.target === popup && !popupContent.contains(event.target)) {
        popup.style.display = "none";
    }
};