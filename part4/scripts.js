document.addEventListener('DOMContentLoaded', () => {
  // Global Variables
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  // ===============================
  // Login Page Logic
  // ===============================
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
          /*const data = await response.json(); */
          document.cookie = `token=${data.access_token}; path=/`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed: ' + response.statusText);
        }
      }catch (err) {
        console.error('Login error:', err);
        alert('An error occurred. Please try again.');
      } 
      } 
    )};


  // ===============================
  // Index Page Logic
  // ===============================
  const placesList = document.getElementById('places-list');

  if (placesList) {
    // 1. Check Authentication (toggles login link)
    checkAuthentication();

    // 2. Fetch Places (Required for Index)
    fetchPlaces(token);

    // 3. Client-Side Filtering
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
      priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placesItems = document.querySelectorAll('.place-card');

        placesItems.forEach(item => {
          const itemPrice = parseInt(item.getAttribute('data-price'));

          if (selectedPrice === 'all' || itemPrice <= parseInt(selectedPrice)) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        });
      });
    }
  }

  // ===============================
  // Place Details Page Logic
  // ===============================
  const placeDetailsSection = document.getElementById('place-details');

  if (placeDetailsSection) {
    checkAuthentication();
    
    // Attempt to redirect unauthenticated user to login page when clicking on view details on index.html (didn't work)
    // if (!token) {
    //   window.location.href = 'login.html';
    // } 
    
    if (placeId) {
      fetchPlaceDetails(token, placeId);
    }
  }

  // ===============================
  // Add Review Page Logic
  // ===============================
  const reviewForm = document.getElementById('review-form');
  const isPlaceDetailsPage = document.getElementById('place-details');

  if (reviewForm) {
    // If not logged in, redirect immediately
    if (!token) {
      if (!isPlaceDetailsPage) {
        window.location.href = 'index.html';
      }
    } else {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const reviewText = document.getElementById('review').value;
        const rating = document.getElementById('rating').value;
        submitReview(token, placeId, reviewText, rating);
      });
    }
  }
});

// ===============================
// Functions
// ===============================

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  // Logic for Login Link (Index Page)
  if (loginLink) {
    if (!token) {
      loginLink.style.display = 'block';
    } else {
      loginLink.style.display = 'none';
    }
  }

  // Logic for Add Review Section (Place Details Page)
  if (addReviewSection) {
    if (!token) {
      addReviewSection.style.display = 'none';
    } else {
      addReviewSection.style.display = 'block';
    }
  }

  return token;
}

async function fetchPlaces(token) {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: headers
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
    } else {
      console.error('Failed to fetch places');
    }
  } catch (err) {
    console.error('Error fetching places:', err);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;
  placesList.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    card.innerHTML = `
      <h3>${place.title}</h3>
      <p>Price: $${place.price}/night</p>
      <p>${place.description}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    placesList.appendChild(card);
  });
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);
    } else {
      console.error('Failed to fetch place details');
    }
  } catch (err) {
    console.error('Error fetching place details:', err);
  }
}

function displayPlaceDetails(place) {
  const placeInfo = document.getElementById('place-info');
  const reviewsSection = document.getElementById('reviews-list');

  if (placeInfo) {
    placeInfo.innerHTML = '';
    const infoContent = document.createElement('div');
    infoContent.innerHTML = `
      <h3>${place.title}</h3>
      <p><strong>Host:</strong> ${place.owner_name || 'Unknown'}</p>
      <p><strong>Price:</strong> $${place.price}/night</p>
      <p><strong>Description:</strong> ${place.description}</p>
      <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.join(', ') : 'None'}</p>
    `;
    placeInfo.appendChild(infoContent);
  }

  if (reviewsSection) {
    reviewsSection.innerHTML = '';
    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(review => {
        const card = document.createElement('div');
        card.className = 'review-card';
        card.innerHTML = `
           <p>${review.comment}</p>
           <p><strong>Rating:</strong> ${review.rating}/5</p>
           <p><small>By: ${review.user_name || 'Unknown'}</small></p>
        `;
        reviewsSection.appendChild(card);
      });
    } else {
      reviewsSection.innerHTML = '<p>No reviews yet.</p>';
    }
  }
}

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        comment: reviewText,
        rating: rating
      })
    });

    if (response.ok) {
      alert('Review submitted successfully!');
      document.getElementById('review-form').reset();
    } else {
      alert('Failed to submit review');
    }
  } catch (err) {
    console.error('Error submitting review:', err);
    alert('An error occurred. Please try again.');
  }
}
