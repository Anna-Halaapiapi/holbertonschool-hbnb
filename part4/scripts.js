// ===============================
// Utility Functions
// ===============================

// Get cookie by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// ===============================
// Login Page Logic
// ===============================
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

  // ===============================
  // Index Page Logic
  // ===============================
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');
  const loginLink = document.getElementById('login-link');

  if (placesList && priceFilter) {
    const token = getCookie('token');

    // Toggle login link visibility
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }

    // Fetch places
    fetch('http://127.0.0.1:5000/api/v1/places', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
      .then(res => res.json())
      .then(places => {
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

        // Initial render
        renderPlaces(places);

        // Price filter logic
        priceFilter.addEventListener('change', () => {
          const selected = priceFilter.value;
          const filtered =
            selected === 'all'
              ? places
              : places.filter(p => p.price <= parseInt(selected));
          renderPlaces(filtered);
        });
      })
      .catch(err => {
        console.error('Error fetching places:', err);
        placesList.innerHTML = '<p>Failed to load places.</p>';
      });
  }

  // ===============================
  // Place Details Page Logic
  // ===============================
  const placeDetails = document.getElementById('place-details');
  const reviewsList = document.getElementById('reviews-list');
  const reviewForm = document.getElementById('review-form');
  const addReviewSection = document.getElementById('add-review');

  if (placeDetails) {
    const token = getCookie('token');
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
      placeDetails.innerHTML = '<p>No place selected.</p>';
      return;
    }

    // Fetch place details
    fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
      .then(res => res.json())
      .then(place => {
        placeDetails.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Host:</strong> ${place.owner_name || 'Unknown'}</p>
        <p><strong>Price:</strong> $${place.price}/night</p>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.join(', ') : 'None'}</p>
      `;
      })
      .catch(() => {
        placeDetails.innerHTML = '<p>Failed to load place details.</p>';
      });

    // Fetch reviews
    fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`)
      .then(res => res.json())
      .then(reviews => {
        reviewsList.innerHTML = '';
        reviews.forEach(r => {
          const card = document.createElement('div');
          card.className = 'review-card';
          card.innerHTML = `
          <p>${r.comment}</p>
          <p><strong>User:</strong> ${r.user_name}</p>
          <p><strong>Rating:</strong> ${r.rating}/5</p>
        `;
          reviewsList.appendChild(card);
        });
      })
      .catch(() => {
        reviewsList.innerHTML = '<p>No reviews available.</p>';
      });

    // Show/hide review form
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';

      // Handle review submission
      reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const comment = document.getElementById('review-text').value;
        const rating = document.getElementById('review-rating').value;

        try {
          const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ comment, rating })
          });

          if (response.ok) {
            alert('Review added!');
            window.location.reload();
          } else {
            const data = await response.json();
            alert(data.msg || 'Failed to add review');
          }
        } catch (err) {
          console.error('Error submitting review:', err);
          alert('An error occurred.');
        }
      });
    }
  }

  // ===============================
  // Add Review Page Logic
  // ===============================
  const placeName = document.getElementById('place-name');

  if (placeName && reviewForm) {
    const token = getCookie('token');
    if (!token) {
      window.location.href = 'index.html';
      return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
      placeName.textContent = 'No place selected.';
      return;
    }

    // Fetch place name
    fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(place => {
        placeName.textContent = `Reviewing: ${place.title}`;
      });

    // Handle form submission
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const comment = document.getElementById('review').value;
      const rating = document.getElementById('rating').value;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({ comment, rating })
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset();
          window.location.href = `place.html?id=${placeId}`;
        } else {
          const data = await response.json();
          alert(data.msg || 'Failed to submit review');
        }
      } catch (err) {
        console.error('Error submitting review:', err);
        alert('An error occurred while submitting your review.');
      }
    });
  }
});
