# HBnB Project: Part 2

This file documents the core backend logic and RESTful API for the HBnB Evolution application, built with Python, Flask, and Flask-RESTx.


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