# 🐞 Manual Testing and Validation of Endpoints

<br>
## 🧍 User Testing

**Step 1**. Create a new user:

```python
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```


**Step 2**. Test Invalid Data for a User

```python
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "", "last_name": "", "email": "invalid-email"}'
```

> Expected output/response `"error": "Invalid input data" // 400 Bad Request`

<br>
## 🏠 Place Testing

### Functionality Testing for Creating, Updating and Retrieving a Place / All Places 

**Step 1**. Create new user:

```python
curl -X POST http://localhost:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Step 2**. Create place:

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```

**Step 3**. Retrieve All Places (GET /api/v1/places)

```python
curl -X GET http://localhost:5000/api/v1/places/ -H "Content-Type: application/json"
```

**Step 4**. Retrieve Place Details (GET /api/v1/places/<place_id>)

```python
curl -X GET http://localhost:5000/api/v1/places/<ENTER_PLACE_ID_HERE> -H "Content-Type: application/json"
```

**Step 5**. Update a Place's Information (PUT /api/places/<place_id>)

```python
curl -X PUT http://localhost:5000/api/v1/places/<ENTER_PLACE_ID_HERE> -H "Content-Type: application/json" -d '{"title":"Luxury Condo","description":"An upscale place to stay","price":200.0}'
```


### Error handling - Retrieving a Non-existent Place

**Step 1**. Retrieve place (with random place ID)

```python
curl -X GET http://localhost:5000/api/v1/places/<ENTER_RANDOM_PLACE_ID_HERE> -H "Content-Type: application/json"
```


### Boundary Testing - Testing Out-of-Range Latitude and Longitude

**Step 1**: Create user:

```python
curl -X POST http://localhost:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Step 2**. Create place with out-of-range latitude (range should be -90.0 to 90.0):

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":97.7749,"longitude":-122.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```


**Step 3**. Create user (again) for out-of-range Longitude testing:

```python
curl -X POST http://localhost:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Step 4**. Create place with out-of-range Longitude (range should be -180.0 - 180.0):

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-192.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```
<br>
### Testing with Missing / Empty values in Required Fields

**Step 1**. Create user:

```python
curl -X POST http://localhost:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

**Step 2**. Create new place with no Title:

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```

**Step 3**. Create user (above) and create place with no Description:

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cyberpunk Apartment","description":"","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```

**Step 4**. Create user (above) and create place with no Price:

```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cyberpunk Apartment","description":"A futuristic, tech-themed rental featuring neon lights!","price":"","latitude":37.7749,"longitude":-122.4194,"owner_id":"<ENTER_OWNER_ID_HERE"}'
```

<br>
## ✍️ Review Testing

### Functionality Testing for Creating, Updating and Deleting a Review


1. Create a user:
```python
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

2. Create a place:
```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"619ef380-9f7c-436b-9ed2-d913d6b530e1"}'
```

3. Create a review:
```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"Great place to stay!","rating":5,"user_id":"e204eaa0-1fd4-4244-802a-8e6e863b0182","place_id":"a997c251-f7cf-4eca-9927-890bd1341a8e"}'
```

4. Retrieve all Reviews:
```python
curl -X GET http://127.0.0.1:5000/api/v1/reviews/
```

5. Retrieve a Single Review by ID
```python
curl -X GET http://127.0.0.1:5000/api/v1/reviews/<review_id>
```

6. Update a Review
```python
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/<review_id> -H "Content-Type: application/json" -d '{"text": "Amazing stay!", "rating": 4}'
```

7. Delete a Review
```python
   curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<review_id>
   ```


8. Get All Reviews for a Specific Place
```python
curl -X GET http://127.0.0.1:5000/api/v1/places/<place_id>/reviews
```


### Test Creating a Review with Empty / Missing Values in Required Fields

1. Create a user:
```python
curl -X POST http://127.0.0.1:5000/api/v1/users/ -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

2. Create a place:
```python
curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{"title":"Cozy Apartment","description":"A nice place to stay","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"619ef380-9f7c-436b-9ed2-d913d6b530e1"}'
```

3. Create a review with missing Text field (content):
```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"","rating":5,"user_id":"e204eaa0-1fd4-4244-802a-8e6e863b0182","place_id":"a997c251-f7cf-4eca-9927-890bd1341a8e"}'
```

3. Create a review with missing Rating:

```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"Awesome place!","rating":"","user_id":"e204eaa0-1fd4-4244-802a-8e6e863b0182","place_id":"a997c251-f7cf-4eca-9927-890bd1341a8e"}'
```

4. Create a review with missing/incorrect User_ID:

```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"Awesome place!","rating":"5","user_id":"","place_id":"a997c251-f7cf-4eca-9927-890bd1341a8e"}'
```

5. Create a review with missing/incorrect Place_ID:

```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"Awesome place!","rating":"5","user_id":"<ENTER_ACTUAL_USER_ID_HERE>","place_id":""}'
```

6. Create a review with rating outside of the review range (>5):

```python
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ -H "Content-Type: application/json" -d '{"text":"Awesome place!","rating":"9","user_id":"<ENTER_ACTUAL_USER_ID_HERE>","place_id":"<ENTER_PLACE_ID_HERE"}'
```


## 🧴 Amenity Testing

1. Create a new Amenity POST

```python
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'
```

**Response:**

```python
{
	"id": "0bdedaa3-b625-4b1c-ac97-c0fdcc4a3e47",
	"name": "Wi-Fi"
}

// 201 Created
```


2. Retrieve an Amenity GET by id

```python
# Replace <paste_your_user_id_here> with the actual ID

curl -X GET http://127.0.0.1:5000/api/v1/amenities/ed855471-ee20-49f0-b791-30d87a4071d2
```

**Response:**

```python
{
	"id": "bf02ca49-8315-4ff6-8cef-881462121f12",
	"name": "Wi-Fi"
}

// 200 OK
```


3. Update Amenity PUT

```python
# Replace <paste_your_user_id_here> with the actual ID

curl -X PUT http://127.0.0.1:5000/api/v1/amenities/ed855471-ee20-49f0-b791- 30d87a4071d2 -H "Content-Type: application/json" -d '{"name": "Air Conditioning"}'
```

**Response:**

```python
{
"message": "Amenity updated successfully"
}

// 200 OK
```

4. Retrieve List of All Amenities GET list

```python
curl -X GET http://127.0.0.1:5000/api/v1/amenities/
```

**Response:**

```python
{
	"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6",
	"name": "Wi-Fi"
},
{
	"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
	"name": "Air Conditioning"
}

// 200 OK
```

