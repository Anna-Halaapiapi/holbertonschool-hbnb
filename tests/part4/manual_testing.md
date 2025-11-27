# Part 4 Testing
### Login Page
#### Test the login functionality with valid and invalid credentials to ensure it works as expected.

Valid input:
```python
127.0.0.1 - - [25/Nov/2025 16:42:15] "POST /api/v1/auth/login HTTP/1.1" 200 -
127.0.0.1 - - [25/Nov/2025 16:42:19] "OPTIONS /api/v1/places HTTP/1.1" 308 -
```
<img width="807" height="455" alt="image" src="https://github.com/user-attachments/assets/a5dfb3de-4cd2-46be-bde1-bcb004737e51" />

Invalid input:
```python
127.0.0.1 - - [25/Nov/2025 16:28:47] "OPTIONS /api/v1/places HTTP/1.1" 308 -
127.0.0.1 - - [25/Nov/2025 16:29:46] "OPTIONS /api/v1/places HTTP/1.1" 308 -
127.0.0.1 - - [25/Nov/2025 16:30:36] "OPTIONS /api/v1/auth/login HTTP/1.1" 200 -
127.0.0.1 - - [25/Nov/2025 16:30:36] "POST /api/v1/auth/login HTTP/1.1" 401 -
```
<img width="865" height="553" alt="image" src="https://github.com/user-attachments/assets/fac320d7-44c1-450f-960b-9ee78e073570" />

#### Verify that the JWT token is stored in the cookie after a successful login.
Output:
<img width="862" height="189" alt="image" src="https://github.com/user-attachments/assets/85533949-47a7-4828-bb97-6b54bcb31946" />

#### Ensure that the user is redirected to the main page after login.
Output:
<img width="822" height="577" alt="image" src="https://github.com/user-attachments/assets/fd509d0f-04af-4510-8501-f9b40996fe02" />
<img width="1185" height="363" alt="image" src="https://github.com/user-attachments/assets/9a2cf93c-4080-4828-9f6f-0dfd16f25244" />


### Index Page
#### Test the functionality by logging in and viewing the list of places.
Unauthenticated user: (list of places appears on the index.html page)
Output:
```python
127.0.0.1 - - [25/Nov/2025 18:52:32] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1666" height="571" alt="image" src="https://github.com/user-attachments/assets/23225026-f1fc-4922-affd-498d670b1d46" />

Authenticated user: (when user is logged in, the list of places shows and the cookie is present with the JWT token)
Output:
```python
127.0.0.1 - - [26/Nov/2025 13:48:42] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [26/Nov/2025 13:48:42] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1673" height="785" alt="image" src="https://github.com/user-attachments/assets/12f1430b-c5d5-48f6-8378-456c2c196683" />

#### Verify that the client-side filter works as expected.
Unauthenticated user (price filters show the correct places, and don’t hit the back end again to update the places that are shown)
‘ALL’ Max Price Filter
Output:
```python
127.0.0.1 - - [25/Nov/2025 19:21:07] "GET /api/v1/places/ HTTP/1.1" 200 -
```

<img width="1679" height="808" alt="image" src="https://github.com/user-attachments/assets/66fe3afd-417d-463c-b80e-a256a853c55b" />
‘10’ Max Price Filter
Output:

```python
127.0.0.1 - - [25/Nov/2025 19:21:07] "GET /api/v1/places/ HTTP/1.1" 200 -
```

<img width="1675" height="606" alt="image" src="https://github.com/user-attachments/assets/16f33cf5-cb87-45ac-bb75-620aabea0232" />
‘50’ Max Price Filter
Output:

```python
127.0.0.1 - - [25/Nov/2025 19:21:07] "GET /api/v1/places/ HTTP/1.1" 200 -
```

<img width="1679" height="627" alt="image" src="https://github.com/user-attachments/assets/637bbf3e-d71a-4b5a-b400-bf97723f07c4" />
‘100’ Max Price Filter

Output:
```python
127.0.0.1 - - [25/Nov/2025 19:21:07] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1673" height="641" alt="image" src="https://github.com/user-attachments/assets/08f26ae4-b53f-41a5-bc9d-3525561c7fe9" />

Authenticated User  (price filters show the correct places, and don’t hit the back end again to update the places that are shown)
 ‘ALL’ Max Price Filter
 
 ```python
127.0.0.1 - - [26/Nov/2025 13:48:42] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [26/Nov/2025 13:48:42] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1665" height="802" alt="image" src="https://github.com/user-attachments/assets/a84f025f-8751-4219-ab5c-836096bd1a09" />

‘10’ Max Price Filter

```python
127.0.0.1 - - [26/Nov/2025 13:48:42] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [26/Nov/2025 13:48:42] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1674" height="574" alt="image" src="https://github.com/user-attachments/assets/11254478-ff28-4c10-927e-c6e51b38845e" />
‘50’ Max Price Filter

```python
127.0.0.1 - - [26/Nov/2025 13:48:42] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [26/Nov/2025 13:48:42] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1671" height="645" alt="image" src="https://github.com/user-attachments/assets/759c4974-f7b7-4c49-b74c-fd9269a9a345" />
‘100’ Max Price Filter

```python
127.0.0.1 - - [26/Nov/2025 13:48:42] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [26/Nov/2025 13:48:42] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1671" height="773" alt="image" src="https://github.com/user-attachments/assets/fe91f0d4-f0a6-4000-acd8-540280f71746" />

#### Ensure the login link appears only when the user is not authenticated. 
Unauthenticated user (login link appears and cookie with JWT token is not present)
```python
127.0.0.1 - - [25/Nov/2025 18:10:40] "GET /api/v1/places/ HTTP/1.1" 200 -
```
<img width="1674" height="415" alt="image" src="https://github.com/user-attachments/assets/93c0496c-595d-4efc-8003-032f0ee4a9a1" />

Authenticated user (login link does not appear and cookie with JWT token is present)
```python
127.0.0.1 - - [25/Nov/2025 18:21:24] "GET /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [25/Nov/2025 18:21:38] "OPTIONS /api/v1/auth/login HTTP/1.1" 200 -
127.0.0.1 - - [25/Nov/2025 18:21:39] "POST /api/v1/auth/login HTTP/1.1" 200 -
127.0.0.1 - - [25/Nov/2025 18:21:40] "OPTIONS /api/v1/places HTTP/1.1" 308 -
```
<img width="1674" height="764" alt="image" src="https://github.com/user-attachments/assets/f2ff01c4-f1a6-4e3d-8f68-bce6c7f52391" />


### Place Page
#### Test the functionality by navigating to the place details page and verifying the displayed information.

Unauthenticated User (cookie not present with JWT token, place details match details from database):
```python
127.0.0.1 - - [27/Nov/2025 11:31:42] "GET /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 11:31:50] "GET /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
```
<img width="1889" height="688" alt="image" src="https://github.com/user-attachments/assets/a9f4d627-03e4-454b-8659-d5ada2959a05" />

Authenticated User (when clicking on View Details from the index.html on a place, the correct place is loaded in the browser. The correct place details are loaded for all 4 places)
```python
127.0.0.1 - - [27/Nov/2025 11:34:48] "OPTIONS /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 11:34:48] "GET /api/v1/places/ HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 11:34:52] "OPTIONS /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 11:34:52] "GET /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
```
<img width="1909" height="621" alt="image" src="https://github.com/user-attachments/assets/bfac082f-48ba-4cba-9043-98ea6796fbec" />

#### Ensure that the add review form appears only when the user is authenticated.
Unauthenticated User:
<img width="1661" height="834" alt="image" src="https://github.com/user-attachments/assets/e0bad036-0103-4b22-8af0-9aaa400834ee" />
Authenticated User:
<img width="1672" height="877" alt="image" src="https://github.com/user-attachments/assets/c7a1aee1-2255-4139-8de0-aed1bb028029" />

### Add Review Page
#### Test the functionality by submitting reviews for a place as an authenticated user.
<img width="1677" height="993" alt="image" src="https://github.com/user-attachments/assets/984a3bf3-2937-4f83-a621-75fbc64522d6" />
Review persisted to the database:

```python
rows = db.session.execute(db.text("SELECT * FROM reviews")).fetchall()
for r in rows:
...     print(dict(r._mapping))
...
{'id': '1a400c71-0c99-4a07-96cb-51028ffa3891', 'text': 'cool place', 'rating': 3, 'place_id': '73248542-bb18-4b36-a04e-a8cf43999249', 'user_id': '41cb9c77-ad8d-4a8c-b81d-9e3030cf91c4', 'created_at': '2025-11-27 11:04:50.011619', 'updated_at': '2025-11-27 11:04:50.011625'}
```

Output:

```python
127.0.0.1 - - [27/Nov/2025 11:04:49] "OPTIONS /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249/reviews HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 11:04:50] "POST /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249/reviews HTTP/1.1" 201 -
127.0.0.1 - - [27/Nov/2025 11:04:51] "GET /api/v1/places/ HTTP/1.1" 200 -
```

#### Verify that unauthenticated users are redirected to the index page.
When an unauthenticated user visits add_review.html, the the user is redirected to index page.
```python
127.0.0.1 - - [27/Nov/2025 11:50:00] "GET /api/v1/places/ HTTP/1.1" 200 -
```
#### Ensure that success and error messages are displayed appropriately.
Authenticated User (submit valid review)
Output:

```python
127.0.0.1 - - [27/Nov/2025 12:04:50] "OPTIONS /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249/reviews HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 12:04:50] "POST /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249/reviews HTTP/1.1" 201 -
127.0.0.1 - - [27/Nov/2025 12:04:51] "GET /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 12:05:07] "OPTIONS /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
127.0.0.1 - - [27/Nov/2025 12:05:07] "GET /api/v1/places/73248542-bb18-4b36-a04e-a8cf43999249 HTTP/1.1" 200 -
```

<img width="1670" height="986" alt="image" src="https://github.com/user-attachments/assets/1dbf02d9-d50d-4577-84fd-48789ca737bc" />




