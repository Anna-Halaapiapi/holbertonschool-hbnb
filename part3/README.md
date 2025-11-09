# DRAFT 
# HBnB Project: Part 3

This version features a persistent database, a complete authentication and authorization system, and a layered architecture built with Flask, Flask-RESTX, and SQLAlchemy.


## 📁 Project Blueprint

```
holbertonschool-hbnb/
├── part1/                      
├── part2/                      
├── part3/                      # Database-backed API with JWT and role-based access
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

## ✅ What's New?

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

## 🚀 Getting Started

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
pip install -r requirements.txt
```
### Run the application 
```bash
python3 run.py
# The server will start on http://127.0.0.1:5000/.
```

## 🔧 Environment Variables

| Variable       | Description                          |
|----------------|--------------------------------------|
| `SECRET_KEY`    | Flask secret key for sessions        |
| `DATABASE_URL`   | SQLAlchemy DB connection string      |

## 🧪 Testing

### Run Unit Tests

```bash
python3 -m app.models.model_tests.user_test
python3 -m app.models.model_tests.place_test
python3 -m app.models.model_tests.amenity_test
```

For detailed endpoint testing instructions, see the
👉[Endpoint Testing Guide](https://github.com/Anna-Halaapiapi/holbertonschool-hbnb/blob/main/tests/part3/task3_endpoint_testing.md)

For detailed SQL script testing instructions, see the
👉[SQL Script Testing Guide](https://github.com/Anna-Halaapiapi/holbertonschool-hbnb/blob/main/tests/part3/task9_sqlscript_testing.md)


## 👥 Authors
- Ashleigh Henna
- Toni Mathieson
- Anna Halaapiapi
- Madison Fleming