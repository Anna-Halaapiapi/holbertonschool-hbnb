# DRAFT 
# HBnB Project: Part 3

This version features a persistent database, a complete authentication and authorization system, and a layered architecture built with Flask, Flask-RESTX, and SQLAlchemy.


## 📁 Project Blueprint

```
HOLBERTONSCHOOL-HBNB/
├── app/
│   ├── __init__.py         
│   ├── api/                # Presentation Layer (API Endpoints)
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/             # Business Logic Layer (Data Models)
│   │   ├── __init__.py
│   │   ├── tests/          # Unit tests for models
│   │   │   ├── amenity_test.py
│   │   │   ├── place_test.py
│   │   │   └── user_test.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/        # Persistence Layer
│   │   ├── __init__.py
│   │   └── repository.py
│   ├── services/           # Business Logic Layer (Operations)
│   │   ├── __init__.py
│   │   └── facade.py
│   └── extensions.py       # Flask extensions (Bcrypt, JWT)
├── tests/                  # Integration/API tests
│   ├── test_endpoints.py
│   └── user-endpoint-testing.md
├── .gitignore
├── config.py               # Configuration file
├── README.md
├── requirements.txt        # Project dependencies
└── run.py                  # Entry point to run the application
```

## 🚀 Key Features

- **Database Persistence**: Fully migrated from in-memory storage to a persistent SQL database using SQLAlchemy and a repository pattern.

- **User Authentication**: Secure user login endpoint using Flask-JWT-Extended to issue JSON Web Tokens.

- **Password Hashing**: User passwords are now securely hashed on creation and verified on login using bcrypt.

- **Role-Based Access Control**: API endpoints are protected based on user roles (e.g., "Admin Only" for creating amenities, "Owner Only" for updating places).

- **Full Data Relationships**: Implemented all one-to-many and many-to-many relationships between users, places, reviews, and amenities.

## 🏗️ Core Features
### Entity Management
- Full CRUD operations for Users, Places, Amenities, and Reviews.
- Business logic validation
- RESTful endpoints with proper HTTP status codes.

### Security & Authentication
- **JWT Token Generation**: Validates credentials against the database and issues signed tokens.
- **Password Hashing**: `bcrypt` is used to securely hash and verify passwords.
- **Protected Routes**: Endpoints are secured using `@jwt_required()`.
- **Admin & User Roles**: `is_admin` claim in the JWT is used to protect admin-only endpoints.

## 📋 Tech Stack & Requirements
- Python
- Flask
- Flask-RESTX
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Bcrypt
- Flask-JWT-Extended
- Pytest

## 📚 API Guide & Endpoints

Once the application is running, visit the URL below to access the interactive Swagger UI. You can view all endpoints, see their required models, and test them directly from your browser.

`http://127.0.0.1:5000/api/v1/`


### Example API Usage

#### Create a new user
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'
```
#### Create a review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "<user-id here>",
    "place_id": "<place-id here>"
  }'
```

## 👥 Authors
- Ashleigh Henna
- Toni Mathieson
- Anna Halaapiapi
- Madison Fleming