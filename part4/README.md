# HBnB Project: Part 4

Part 4 of our HBNB project focuses on integrating the back-end with a functional browser-based user interface. After building the database, models, and authenticated API in Part 3, Part 4 adds a simple but functional front-end that communicates directly with the server. Users can log in, view places, and submit a review through our Javascript fetch calls handled in the browser. 

## Project Blueprint

```
holbertonschool-hbnb/
├── part1/                      
├── part2/                      
├── part3/                      # Database-backed API with JWT and role-based access
├── part4/                      # Client side front-end
│   ├── app/
│   │   ├── __init__.py         # Flask app factory
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── amenities.py
│   │   │       ├── auth.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       └── users.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── amenity.py
│   │   │   ├── base_model.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   │   └── model_tests/
│   │   │       ├── __init__.py
│   │   │       ├── amenity_test.py
│   │   │       ├── place_test.py
│   │   │       └── user_test.py
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   └── repository.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── facade.py
│   │   │   └── extensions.py
│   ├── config.py               # App and DB configuration
│   ├── initial_data.sql        # Sample data for DB seeding
│   ├── add_review.html         # Add Review form template
│   ├── index.html              # Home page template
│   ├── p4_seed_file.sql        # Sample data for DB seeding
│   ├── login.html              # Login landing page template
│   ├── place.html              # Place landing page template
│   ├── scripts.js              # Javascript AJAX requests and client side rendering
│   ├── styles.css              # CSS styling
│   ├── tables.sql              # SQL schema definition
│   ├── requirements.txt        # Project dependencies
│   ├── run.py                  # App entry point
│   ├── README.md               # Project documentation
│   ├── ER_Diagrams.png         # Mermaid-generated schema diagram
│   └── tests/
│       ├── part2/              # Legacy tests from part 2
│       ├── part3/              # Tests for JWT, DB, and relationships
│       ├── task3_endpoint_testing.md
│       └── task9_sqlscript_testing.md

```

## What's New?

- **Client-Side Front-end**: User-friendly interface and client side rendering that consumes the API created in part 3.

- **API Calls**: The back-end API now communicates with the front-end using AJAX Fetch requests.

- **HTML Templates**: Added templates for login, home page, place listings and review creation.

- **Authentication**: JWT authentication is now integrated into the browser using Local Storage.

- **Dynamic Rendering**: Javascript now handles API calls, token storage, DOM updates and user interactions.
  
## Core Features

### Front-end Features
- Functional login page that calls the auth/login endpoint with Fetch
- Place details page that loads place, reviews, amenities dynamically from the API response
- Add review form page that submits reviews using authenticated fetch requests
- Javascript file to dynamically load data into the html page
- CSS styling for layout and user interface
- Client side validation and error handling

### Entity Management
- Full CRUD operations for Users, Places, Amenities, and Reviews.
- Business logic validation
- RESTful endpoints with proper HTTP status codes.

### Security & Authentication
- **JWT Token Generation**: Javascript now sends the JWT in an Authorization Header for secure requests
- **Login**: User sessions persist in the browser using Local Storage
- **Logout**: Clearing local storage will log the user out and redirects back to the login page.
- **Unauthorised Access**: If a User is unauthorized to perform a request, they will be redirected or blocked from the request.
- **Password Hashing**: `bcrypt` is used to securely hash and verify passwords.
- **Protected Routes**: Endpoints are secured using `@jwt_required()`.
- **Admin & User Roles**: `is_admin` claim in the JWT is used to protect admin-only endpoints.

## Getting Started

### Clone the repository
```bash
git clone https://github.com/Anna-Halaapiapi/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```
### Create a virtual environment 
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
### Install dependencies
```bash
cd part4
pip install -r requirements.txt
```
### Start the application
```bash
python3 run.py

# The server will start on http://127.0.0.1:5000/.
# The SQLite database (development.db) and tables will be created in this step
```
### Stop the application
```bash
CTRL + C
```
### Seed the initial data
```bash
sqlite3 instance/development.db < p4_seed_file.sql
```
### Run the application
```bash
python3 run.py
```
### Open the login page to view the user interface
```bash
### screenshot open with live server
```
### Login as a user
```bash
### screenshot login page
```
### View Place Details
```bash
### view place details
```
### Leave a Review
```bash
### leave a review page
```

### Testing
https://github.com/Anna-Halaapiapi/holbertonschool-hbnb/blob/main/tests/part4/manual_testing.md

### Run Unit Tests
```bash
python3 -m app.models.model_tests.user_test
python3 -m app.models.model_tests.place_test
python3 -m app.models.model_tests.amenity_test
```

## Authors
- Ashleigh Henna
- Toni Mathieson
- Anna Halaapiapi
- Madison Fleming

