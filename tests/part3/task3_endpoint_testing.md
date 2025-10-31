# 🐞 Task 3 - Authenticated and Public Endpoint Testing
**Intro**  
The purpose of this document is to outline the testing that was performed for Part 3, Task 3 of the HBnB project, along with testing outcomes. All tests were performed using cURL commands.

**Objective**  
The goal was to verify that all authenticated API endpoints were correctly secured with JWT authentication, and that public endpoints remained accessible without a JWT token.

**Part One - Tests for Authenticated Endpoints**   
This part ensures that only authorised users are able to create, update, or delete resources such as Places, Reviews, and User details.

**Part Two - Tests for Public Endpoints**  
This part ensures that public routes (such as retrieving a list of places, or retrieving info about a specific place) are accessible without JWT authentication.

**Outcome**  
All tests returned the expected HTTP status codes and responses, confirming that the authentication and authorisation logic has been implemented correctly.


## PART ONE - AUTHENTICATED ENDPOINT TESTING
## # 1. Test Place Creation (POST /api/v1/places/)
### <u>Create a place as an authenticated user</u>
The aim of this test is to verify that a user who is logged in (authenticated) can create a new place.
### Step 1: Create a new user (User A)
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -d '{"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "password": "password123"}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
    "id": "0a1ab...",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
}
```

### Step 2: Log in as User A and copy your JWT token
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -d '{"email": "jane.doe@example.com", "password": "password123"}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
  "access_token": "eyJhb..."
}
```
### Step 3: Create a new place as authenticated User A using your JWT token.
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -d '{"title": "New Place", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "amenities": []}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:** \
Note: Take note of id (place id)
```json
{
    "id": "7e32f...",
    "title": "New Place",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "0a1ab...",
    "amenities": [],
    "reviews": []
}
```
### <u>Create a place as an unauthenticated user</u>
The aim of this test is to verify that a user who is not logged in (unauthenticated) cannot create a new place.
### Step 1: Attempt to create a new place
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -d '{"title":"Unauthorized User Place","description":"Unauthorized User Place Description","price":50.0,"latitude":10.0,"longitude":20.0,"amenities":[]}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```
## # 2. Test Unauthorized Place Update (PUT /api/v1/places/<place_id>)
### <u>Update a place as an unauthorized user</u>
The aim of this test is to verify that a user cannot update a place they do not own.

### Step 1: Create a new user (User B)
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -d '{"first_name": "Johnny", "last_name": "Doe", "email": "johnny.doe@example.com", "password": "password123"}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
    "id": "2371d...",
    "first_name": "Johnny",
    "last_name": "Doe",
    "email": "johnny.doe@example.com"
}
```

### Step 2: Log in as new User B and copy your JWT token
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -d '{"email": "johnny.doe@example.com", "password": "password123"}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
  "access_token": "eyJhb..."
}
```
### Step 3: Try update User A's place as unauthorized User B
**Command:**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/places/USER_A_PLACE_ID" -d '{"title": "Updated Place"}' -H "Authorization: Bearer USER_B_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 403 FORBIDDEN
```
```json
{
    "error": "Unauthorized action"
}
```
### <u>Update a place as an authorized user</u>
### Step 1: Logged in as User A, update User A's place
**Command:**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/places/USER_A_PLACE_ID" -d '{"title": "Updated Place"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Output:**
```bash
> HTTP/1.1 200 OK
```
```json
{
    "id": "7e32f...",
    "title": "Updated Place",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "0a1ab...",
    "amenities": [],
    "reviews": []
}
```
## # 3. Test Creating a Review (POST /api/v1/reviews/)
### <u>Create a review as an authenticated user</u>
The aim of this test is to verify that a logged in (authenticated) user can create a review for a place they don't own.
### Step 1: Logged in as User B, review User A's place
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -d '{"place_id": "USER_A_PLACE_ID","text": "Great place!", "rating": 5, "user_id": "placeholder"}' -H "Authorization: Bearer USER_B_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
    "id": "f98b7...",
    "text": "Great place!",
    "rating": 5,
    "user_id": "2371d...",
    "place_id": "7e32f..."
}
```
### <u>Create a review as an unauthenticated user</u>
The aim of this test is to verify that individuals that aren't logged in (unauthenticated) are unable to create a review.\
**Command:**
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -d '{"place_id": "USER_A_PLACE_ID", "text": "This is an unauthorized review attempt!", "rating": 4, "user_id": "placeholder"}' -H "Content-Type: application/json"
```
**Expected Response:**
```json
{
  "msg": "Missing Authorization Header"
}
```
### <u>Create a review on your own place</u>
The aim of this test is to verify that a place owner is unable to leave a review on their own property.
### Step 1: Logged in as User A, leave a review on User A's place
**Command:**
```bash
curl -v -X POST "http://127.0.0.1:5000/api/v1/reviews/" -d '{"place_id": "USER_A_PLACE_ID", "text": "This is my own place!", "rating": 5, "user_id": "placeholder"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 400 BAD REQUEST
```
```json
{
    "error": "You cannot review your own place."
}
```
### <u>Create another review on the same place</u>
The aim of this test is to verify that a user cannot review the same place more than once.
### Step 1: Logged in as User B, leave a second review on User A's place
**Command:**
```bash
curl -v -X POST "http://127.0.0.1:5000/api/v1/reviews/" -d '{"place_id": "USER_A_PLACE_ID", "text": "This is another review for same place!", "rating": 5, "user_id": "placeholder"}' -H "Authorization: Bearer USER_B_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 400 BAD REQUEST
```
```json
{
    "error": "You have already reviewed this place."
}
```
## #4. Test Updating a Review (PUT /api/v1/reviews/<review_id>)
### <u>Update a review as an authorized user</u>
The aim of this test is to verify that an authorized user can update their own review.
### Step 1: Logged in as User B, update User B's review
**Command:**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/reviews/USER_B_REVIEW_ID" -d '{"text": "Updated review", "rating": 4}' -H "Authorization: Bearer USER_B_TOKEN" -H "Content-Type: application/json"
```
**Expected Response**
```bash
> HTTP/1.1 200 OK
```
```json
{
    "id": "f98b....",
    "text": "Updated review",
    "rating": 4,
    "user_id": "2371...",
    "place_id": "7e3..."
}
```
### <u>Update a review as an unauthorized user</u>
The aim of this test is to verify that an unauthorized user is unable to update a review.
### Step 1: Logged in as User A, attempt an update on User B's review
**Command:**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/reviews/USER_B_REVIEW_ID" -d '{"text": "Trying to change someone else’s review"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 403 FORBIDDEN
```
```json
{
    "error": "Unauthorized action."
}
```
## #5. Test Deleting a Review (DELETE /api/v1/reviews/<review_id>)
### <u>Delete another user's review</u>
The aim of this test is to verify that an unauthorized user cannot delete another user's review.
### Step 1: Logged in as User A, attempt to delete User B's review
**Command:**
```bash
curl -v -X DELETE "http://127.0.0.1:5000/api/v1/reviews/USER_B_REVIEW_ID" -H "Authorization: Bearer USER_A_TOKEN"
```
**Expected output**
```bash
> HTTP/1.1 403 FORBIDDEN
```
```json
{
    "error": "Unauthorized action."
}
```
### <u>Delete your own review</u>
The aim of this test is to verify that an authorized user can delete their own review.
### Step 1: Logged in as User B, delete User B's review
**Command**
```bash
curl -v -X DELETE "http://127.0.0.1:5000/api/v1/reviews/USER_B_REVIEW_ID" -H "Authorization: Bearer USER_B_TOKEN"
```
**Expected Response:**
```bash
> HTTP/1.1 200 OK
```
```json
{
    "message": "Review deleted successfully"
}
```
## #6. Test Modifying User Data (PUT /api/v1/users/<user_id>)
### <u>A user can update their own details</u>
The aim of this test is to verify that an authorized user is able to update their own personal details (excluding their email and password)
### Step 1: Logged in as User A, attempt to update User A's first name
**Command:**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/users/USER_A_ID" -d '{"first_name": "Janey"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 200 OK
```
```json
{
    "id": "0a1...",
    "first_name": "Janey",
    "last_name": "Doe"
}
```
### <u>A user cannot update another user's details</u>
The aim of this test is to verify that a user (unauthorized) is unable to update another user's personal details.
### Step 1: As User B, attempt to update User A's details
**Command**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/users/USER_A_ID" -d '{"first_name": "HackersName"}' -H "Authorization: Bearer USER_B_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 403 FORBIDDEN
```
```json
{
    "error": "Unauthorized action."
}
```
### <u>Attempt to modify restricted field (email)</u>
The aim of this test is to verify that a user (authorized) is unable to update a restricted field (email).
### Step 1: As User A, attempt to update User A's email address
**Command**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/users/USER_A_ID" -d '{"email": "new.email@example.com"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 400 BAD REQUEST
```
```json
{
    "error": "You cannot modify email or password."
}
```
### <u>Attempt to modify restricted field (password)</u>
The aim of this test is to verify that a user (authorized) is unable to update a restricted field (password).
### Step 1: As User A, attempt to update User A's password
**Command**
```bash
curl -v -X PUT "http://127.0.0.1:5000/api/v1/users/USER_A_ID" -d '{"password": "mynewpassword123"}' -H "Authorization: Bearer USER_A_TOKEN" -H "Content-Type: application/json"
```
**Expected Response:**
```bash
> HTTP/1.1 400 BAD REQUEST
```
```json
{
    "error": "You cannot modify email or password."
}
```
## PART TWO - PUBLIC ENDPOINT TESTING
## # 7. Public endpoint: GET /api/v1/places/
### <u>Retrieve a list of places</u>
The aim of this test is to verify accessibility to retrieving a list of places without a JWT Token.\
**Command:**
```bash
curl -v -X GET "http://127.0.0.1:5000/api/v1/places/"
```
**Expected Response:**
```bash
> HTTP/1.1 200 OK
```
```json
[
    {
        "id": "7e3...",
        "title": "Updated Place",
        "description": "A nice place to stay",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": "0a1a...",
        "amenities": [],
        "reviews": []
    }
]
```
## # 8. Public endpoint: GET /api/v1/places/<place_id>
### <u>Retrieve detailed information about a specific place</u>
The aim of this test is to verify accessibility to getting detailed information about a specific place without a JWT Token.
**Command**
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/places/PLACE_ID"
```
**Expected Response:**
```bash
> HTTP/1.1 200 OK
```
```json
{
    "id": "7e3...",
    "title": "Updated Place",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "0a1...",
    "amenities": [],
    "reviews": []
}
```