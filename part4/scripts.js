// Utility: Get cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Login form handler
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
          // Store JWT in cookie
          document.cookie = `token=${data.access_token}; path=/`;
          alert('Login successful!');
          window.location.href = 'index.html'; // redirect to places list
        } else {
          alert(data.msg || 'Login failed');
        }
      } catch (err) {
        console.error('Error:', err);
        alert('An error occurred. Please try again.');
      }
    });
  }
});
