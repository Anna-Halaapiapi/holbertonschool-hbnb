// Utility: Get cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// Login Form Logic
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
          document.cookie = `token=${data.access_token}; path=/`;
          alert('Login successful!');
          window.location.href = 'index.html';
        } else {
          alert(data.msg || 'Login failed');
        }
      } catch (err) {
        console.error('Login error:', err);
        alert('An error occurred. Please try again.');
      }
    });
  }

  // Places List Logic
  const placesList = document.getElementById('places-list');
  const countryFilter = document.getElementById('country-filter');

  if (placesList && countryFilter) {
    const token = getCookie('token');
    if (!token) {
      window.location.href = 'login.html';
      return;
    }

    fetch('http://127.0.0.1:5000/api/v1/places', {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(places => {
        const countries = [...new Set(places.map(p => p.country))];
        countries.forEach(country => {
          const option = document.createElement('option');
          option.value = country;
          option.textContent = country;
          countryFilter.appendChild(option);
        });

        function renderPlaces(filteredPlaces) {
          placesList.innerHTML = '';
          filteredPlaces.forEach(place => {
            const card = document.createElement('div');
            card.className = 'place-card';
            card.innerHTML = `
              <h3>${place.title}</h3>
              <p>Price: $${place.price}/night</p>
              <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(card);
          });
        }

        renderPlaces(places);

        countryFilter.addEventListener('change', () => {
          const selected = countryFilter.value;
          const filtered = selected ? places.filter(p => p.country === selected) : places;
          renderPlaces(filtered);
        });
      })
      .catch(err => {
        console.error('Error fetching places:', err);
        placesList.innerHTML = '<p>Failed to load places.</p>';
      });
  }
});
