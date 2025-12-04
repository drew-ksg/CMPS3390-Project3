document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username, password})
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('jwt', data.access_token);
            window.location.href = '/dashboard';
        } else {
            alert("Invalid credentials, please try again." + data.detail);
        }
    }   catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    }



});