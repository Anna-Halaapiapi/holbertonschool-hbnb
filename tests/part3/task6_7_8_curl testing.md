**CURL Testing for Part 3**

---
**Login as an Authorised User**

```python
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" -d '{"email": "[admin@example.com](mailto:admin@example.com)", "password": "adminpassword"}' -H "Content-Type: application/json"
```

**Get Token**

```python
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNzQ0MCwianRpIjoiMTM1MDUwOWMtZmNiYi00M2FiLTg3MjItYWNiMTQ5YzZkODRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjcwMTMwNTBkLTEwNjgtNGU3MC04ZDdmLTIyNGRhZmQ3ZjMzOSIsIm5iZiI6MTc2MjgxNzQ0MCwiY3NyZiI6ImE1YmU0NjIxLTJmZGMtNDNkOC1hNjJhLTQyZTBmOGQyOTA5ZSIsImV4cCI6MTc2MjgxODM0MCwiaXNfYWRtaW4iOnRydWV9.qDah2FTm1ZyVJ9C5jL02NHcRDuPdw2hdv-hJy4Z_jlI
```
**login as a Normal User**

```python
curl -X POST "[http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/auth/login)auth/login" -d '{"email": "[john.doe@example.com](mailto:john.doe@example.com)", "password": "password123"}' -H "Content-Type: application/json"
```
**Get User Access Token**

```python
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQ5MSwianRpIjoiMjVlZGU5YzAtZDRhNy00N2MwLWIzNjEtM2RiOTVlOTAwYWJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjRhY2IxZDNkLTk0MWYtNDQxNS04MzYxLWIxOGIzMzhhYjYyYyIsIm5iZiI6MTc2MjgxNTQ5MSwiY3NyZiI6IjhiNzg0ZTM4LTNlZmYtNDQ2Zi1iY2MzLWY3ZDA2NmJiMzQwZiIsImV4cCI6MTc2MjgxNjM5MSwiaXNfYWRtaW4iOmZhbHNlfQ.BnzPxdy7-9BA7YDfuG8rQD8EPGSTviSb2oUSx61vAgw
```

**Test User Creation** 

```
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQxNiwianRpIjoiOTk5YWU5ZTEtZTY1Ny00MjNhLThiN2ItOWFhMGRlYWQ0MjAwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjNmZjQ2ZDk3LTViMGQtNGE4Ny1hM2NhLWU3ZGYxYTMzN2Y0NCIsIm5iZiI6MTc2MjgxNTQxNiwiY3NyZiI6IjlmYzlkZTA1LTdlMjEtNDAyOC05MDFmLTUyMWJlMTFkNGFjNyIsImV4cCI6MTc2MjgxNjMxNiwiaXNfYWRtaW4iOnRydWV9.DrSlxQ1d8J0FpY-qVLkJi5719-R9nLLscpFolaZL39U"
```
**Output:**

```python
{
	"id": "ff6faa34-406c-449f-98ae-98cb5d84db97",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
}
```
**Test Invalid User Creation**

```
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "email": "john.doe@example.com",
  "password": ""
}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjY4MzM4NiwianRpIjoiMDNhMmQzZGQtYTU1NC00YmYyLTlmZWMtMDE1MjRkM2E1NjUzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImQyMzM1YjY2LTM3MjQtNDgxOC04YmRhLTY3NzhlNWJkNDkxOSIsIm5iZiI6MTc2MjY4MzM4NiwiY3NyZiI6ImJmYTNjN2YxLTM1YTItNGRmZC04ZWY5LTg3ZTc0ZDkzNWI0ZSIsImV4cCI6MTc2MjY4NDI4NiwiaXNfYWRtaW4iOnRydWV9.CZzTLQSsjQs7JgE0SqK9BhxnUNp4qRPCHp2lPVGEzeI"
```
**Output:**

```python
{
"errors": {
"last_name": "'last_name' is a required property"
},
"message": "Input payload validation failed
```
**Retrieve the user by ID**

```python
curl -X GET "http://127.0.0.1:5000/api/v1/users/758aa033-5cc4-41b3-b82e-0a22b7c8377a" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjY4MzM4NiwianRpIjoiMDNhMmQzZGQtYTU1NC00YmYyLTlmZWMtMDE1MjRkM2E1NjUzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImQyMzM1YjY2LTM3MjQtNDgxOC04YmRhLTY3NzhlNWJkNDkxOSIsIm5iZiI6MTc2MjY4MzM4NiwiY3NyZiI6ImJmYTNjN2YxLTM1YTItNGRmZC04ZWY5LTg3ZTc0ZDkzNWI0ZSIsImV4cCI6MTc2MjY4NDI4NiwiaXNfYWRtaW4iOnRydWV9.CZzTLQSsjQs7JgE0SqK9BhxnUNp4qRPCHp2lPVGEzeI"
```
**Output:**

```python
{
"id": "ff6faa34-406c-449f-98ae-98cb5d84db97",
"first_name": "John",
"last_name": "Doe",
"email": "[john.doe@example.com](mailto:john.doe@example.com)"
}
```

**Update a User’s Information**

```
curl -X PUT "http://127.0.0.1:5000/api/v1/users/e4b08b76-fb8e-4343-a28c-20575de2d77f" -H "Content-Type: application/json" -d '{"first_name": "Josh", "last_name": "Smith", "email": "josh.doe@example.com"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2Mjc0MDAzNSwianRpIjoiZTIwN2UwNTktNTEzMS00MDE3LTgzMTctOGM5MTU4YzU4NDlmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Ijc5N2E3NWFkLTYxOWUtNDdlMy04NjgxLTA1NzdhZjA1Zjk1ZiIsIm5iZiI6MTc2Mjc0MDAzNSwiY3NyZiI6ImJiMDljMmFlLWIyYTAtNDFkMy05MWJjLTFkYjc5ZjE0N2RlZSIsImV4cCI6MTc2Mjc0MDkzNSwiaXNfYWRtaW4iOnRydWV9.EUlmbuEjYL5SUz9LS2yTndqLKDTBZvSso02TLa3iU5s"
```
**Outcome:**

```python
{
"id": "e4b08b76-fb8e-4343-a28c-20575de2d77f",
"first_name": "Josh",
"last_name": "Smith",
"email": "[josh.doe@example.com](mailto:josh.doe@example.com)"
}
```

**Place Creation**

```python
curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Bed and Breakfast", "description": "A great place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNzQ0MCwianRpIjoiMTM1MDUwOWMtZmNiYi00M2FiLTg3MjItYWNiMTQ5YzZkODRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjcwMTMwNTBkLTEwNjgtNGU3MC04ZDdmLTIyNGRhZmQ3ZjMzOSIsIm5iZiI6MTc2MjgxNzQ0MCwiY3NyZiI6ImE1YmU0NjIxLTJmZGMtNDNkOC1hNjJhLTQyZTBmOGQyOTA5ZSIsImV4cCI6MTc2MjgxODM0MCwiaXNfYWRtaW4iOnRydWV9.qDah2FTm1ZyVJ9C5jL02NHcRDuPdw2hdv-hJy4Z_jlI"
```
**Output:**

```python
{
    "id": "9ee960f5-4c22-419e-973a-7d0584463a53",
    "title": "Bed and Breakfast",
    "description": "A great place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "b014e2a5-1019-46d3-aade-baac0ace7df7",
        "first_name": "Super",
        "last_name": "Admin",
        "email": "admin@example.com"
    },
    "amenities": [],
    "reviews": []
}
```
**Retrieve Place by ID**

```python
curl -X GET "http://127.0.0.1:5000/api/v1/places/712715da-16df-41a4-bba1-f8a1c5271b81" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2Mjc0ODU5NywianRpIjoiY2NhMjQyMzQtOGViYi00M2Q0LTkxNGItNjc3MmFmOTA1YWQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImQ4YjZjMDEzLWNiNzctNGEwZi04YmQzLTlkNmM3NjI5NWI3ZiIsIm5iZiI6MTc2Mjc0ODU5NywiY3NyZiI6ImNiMmU4ZjliLTM4OTUtNDc3MC1iZjBjLTQ0MmI4ZGE1NDEwNiIsImV4cCI6MTc2Mjc0OTQ5NywiaXNfYWRtaW4iOnRydWV9.wre72kn9pnVD8AJIWshr_5dMNk75bZWxKXvRtE15kLc"
```

**Output:**

```python
{
    "id": "712715da-16df-41a4-bba1-f8a1c5271b81",
    "title": "Bed and Breakfast",
    "description": "A great place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "d8b6c013-cb77-4a0f-8bd3-9d6c76295b7f",
        "first_name": "Super",
        "last_name": "Admin",
        "email": "admin@example.com"
    },
    "amenities": [],
    "reviews": []
}
```
**Update a Place’s Information**

```
curl -X PUT "http://127.0.0.1:5000/api/v1/places/9ee960f5-4c22-419e-973a-7d0584463a53" -H "Content-Type: application/json" -d '{"title": "Luxury Condo", "description": "An upscale place to stay"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNzQ0MCwianRpIjoiMTM1MDUwOWMtZmNiYi00M2FiLTg3MjItYWNiMTQ5YzZkODRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjcwMTMwNTBkLTEwNjgtNGU3MC04ZDdmLTIyNGRhZmQ3ZjMzOSIsIm5iZiI6MTc2MjgxNzQ0MCwiY3NyZiI6ImE1YmU0NjIxLTJmZGMtNDNkOC1hNjJhLTQyZTBmOGQyOTA5ZSIsImV4cCI6MTc2MjgxODM0MCwiaXNfYWRtaW4iOnRydWV9.qDah2FTm1ZyVJ9C5jL02NHcRDuPdw2hdv-hJy4Z_jlI"
```
**Output:**

```python
{
    "id": "9ee960f5-4c22-419e-973a-7d0584463a53",
    "title": "Luxury Condo",
    "description": "An upscale place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner": {
        "id": "d8b6c013-cb77-4a0f-8bd3-9d6c76295b7f",
        "first_name": "Super",
        "last_name": "Admin",
        "email": "admin@example.com"
    },
    "amenities": [],
    "reviews": []
}
```
**Test Review Creation and Retrieval** 

```
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Content-Type: application/json" -d '{"text": "Great place to stay!", "rating": 5, "user_id": "4acb1d3d-941f-4415-8361-b18b338ab62c", "place_id": "4892be7b-390c-44a9-94e9-a4450e4ba625"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQ5MSwianRpIjoiMjVlZGU5YzAtZDRhNy00N2MwLWIzNjEtM2RiOTVlOTAwYWJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjRhY2IxZDNkLTk0MWYtNDQxNS04MzYxLWIxOGIzMzhhYjYyYyIsIm5iZiI6MTc2MjgxNTQ5MSwiY3NyZiI6IjhiNzg0ZTM4LTNlZmYtNDQ2Zi1iY2MzLWY3ZDA2NmJiMzQwZiIsImV4cCI6MTc2MjgxNjM5MSwiaXNfYWRtaW4iOmZhbHNlfQ.BnzPxdy7-9BA7YDfuG8rQD8EPGSTviSb2oUSx61vAgw"
```

**Output:**

```python
{
    "id": "21945603-4f34-4457-a340-390e9c0a0406",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "4acb1d3d-941f-4415-8361-b18b338ab62c",
    "place_id": "4892be7b-390c-44a9-94e9-a4450e4ba625"
}
```

**Retrieve the Review by ID**

```python
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/21945603-4f34-4457-a340-390e9c0a0406" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQ5MSwianRpIjoiMjVlZGU5YzAtZDRhNy00N2MwLWIzNjEtM2RiOTVlOTAwYWJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjRhY2IxZDNkLTk0MWYtNDQxNS04MzYxLWIxOGIzMzhhYjYyYyIsIm5iZiI6MTc2MjgxNTQ5MSwiY3NyZiI6IjhiNzg0ZTM4LTNlZmYtNDQ2Zi1iY2MzLWY3ZDA2NmJiMzQwZiIsImV4cCI6MTc2MjgxNjM5MSwiaXNfYWRtaW4iOmZhbHNlfQ.BnzPxdy7-9BA7YDfuG8rQD8EPGSTviSb2oUSx61vAgw"
```

**Output:**

```python
{
    "id": "21945603-4f34-4457-a340-390e9c0a0406",
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "4acb1d3d-941f-4415-8361-b18b338ab62c",
    "place_id": "4892be7b-390c-44a9-94e9-a4450e4ba625"
}
```

**Update a review’s information**

```
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/21945603-4f34-4457-a340-390e9c0a0406" -H "Content-Type: application/json" -d '{"text": "Amazing stay!", "rating": 4}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQ5MSwianRpIjoiMjVlZGU5YzAtZDRhNy00N2MwLWIzNjEtM2RiOTVlOTAwYWJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjRhY2IxZDNkLTk0MWYtNDQxNS04MzYxLWIxOGIzMzhhYjYyYyIsIm5iZiI6MTc2MjgxNTQ5MSwiY3NyZiI6IjhiNzg0ZTM4LTNlZmYtNDQ2Zi1iY2MzLWY3ZDA2NmJiMzQwZiIsImV4cCI6MTc2MjgxNjM5MSwiaXNfYWRtaW4iOmZhbHNlfQ.BnzPxdy7-9BA7YDfuG8rQD8EPGSTviSb2oUSx61vAgw"
```

**Output:**

```python
{
"id": "21945603-4f34-4457-a340-390e9c0a0406",
"text": "Amazing stay!",
"rating": 4,
"user_id": "4acb1d3d-941f-4415-8361-b18b338ab62c",
"place_id": "4892be7b-390c-44a9-94e9-a4450e4ba625"
}
```

**Delete a Review**

```python
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/21945603-4f34-4457-a340-390e9c0a0406" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNTQ5MSwianRpIjoiMjVlZGU5YzAtZDRhNy00N2MwLWIzNjEtM2RiOTVlOTAwYWJmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjRhY2IxZDNkLTk0MWYtNDQxNS04MzYxLWIxOGIzMzhhYjYyYyIsIm5iZiI6MTc2MjgxNTQ5MSwiY3NyZiI6IjhiNzg0ZTM4LTNlZmYtNDQ2Zi1iY2MzLWY3ZDA2NmJiMzQwZiIsImV4cCI6MTc2MjgxNjM5MSwiaXNfYWRtaW4iOmZhbHNlfQ.BnzPxdy7-9BA7YDfuG8rQD8EPGSTviSb2oUSx61vAgw"
```

**Output:**

```python
{
"message": "Review deleted successfully"
}
```
**Test Amenity Creation** 

```
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNzQ0MCwianRpIjoiMTM1MDUwOWMtZmNiYi00M2FiLTg3MjItYWNiMTQ5YzZkODRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjcwMTMwNTBkLTEwNjgtNGU3MC04ZDdmLTIyNGRhZmQ3ZjMzOSIsIm5iZiI6MTc2MjgxNzQ0MCwiY3NyZiI6ImE1YmU0NjIxLTJmZGMtNDNkOC1hNjJhLTQyZTBmOGQyOTA5ZSIsImV4cCI6MTc2MjgxODM0MCwiaXNfYWRtaW4iOnRydWV9.qDah2FTm1ZyVJ9C5jL02NHcRDuPdw2hdv-hJy4Z_jlI"
```

**Output:**

```python
{
"id": "bbf4767d-dedc-453b-89cc-f7da32f930e7",
"name": "Wi-Fi"
}
```

**Retrieve the Amenity by ID**

```python
curl -X GET "http://127.0.0.1:5000/api/v1/amenities/bbf4767d-dedc-453b-89cc-f7da32f930e7"
```

**Output:**

```python
{
"id": "bbf4767d-dedc-453b-89cc-f7da32f930e7",
"name": "Wi-Fi"
}
```

**Update an Amenities information**

```
curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/bbf4767d-dedc-453b-89cc-f7da32f930e7" -H "Content-Type: application/json" -d '{"name": "Ensuite"}' -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MjgxNzQ0MCwianRpIjoiMTM1MDUwOWMtZmNiYi00M2FiLTg3MjItYWNiMTQ5YzZkODRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjcwMTMwNTBkLTEwNjgtNGU3MC04ZDdmLTIyNGRhZmQ3ZjMzOSIsIm5iZiI6MTc2MjgxNzQ0MCwiY3NyZiI6ImE1YmU0NjIxLTJmZGMtNDNkOC1hNjJhLTQyZTBmOGQyOTA5ZSIsImV4cCI6MTc2MjgxODM0MCwiaXNfYWRtaW4iOnRydWV9.qDah2FTm1ZyVJ9C5jL02NHcRDuPdw2hdv-hJy4Z_jlI" 
```

**Output:**

```python
{
"id": "bbf4767d-dedc-453b-89cc-f7da32f930e7",
"name": "Ensuite"
}
```
