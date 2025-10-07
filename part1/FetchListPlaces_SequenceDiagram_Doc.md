# Fetch a List of Places - Sequence Diagram Documentation

### Purpose
This sequence diagram describes the steps involved when a user requests a list of places in the HBnB Evolution system.
It illustrates the flow of information across the Presentation, Business Logic and Persistence layers.

### Components

|Actor|Layer|Role|
|---|---|---|
|`User`|Client|Initiates the request via web/browser|
|`PlaceAPI`|Presentation Layer|Receives and handles the HTTP GET request|
|`PlaceService`|Business Logic Layer|Coordinates logic and filter processing|
|`PlaceRepository`|Persistence Layer|Fetches place data from the database|
|`AmenityRepository`|Persistence Layer (optional)|(If included) Fetches amenities for places|

### Flow of Events

1. User sends a `GET /places?location=melbourne&price=450` request to the API

2. `PlaceAPI` parses the query parameters (converting HTTP request into Python format).

3. `PlaceAPI` calls `get_places(filters)` from `PlaceService` to retrieve matching places.

4. `PlaceService` enforces application rules (e.g. checks if location is valid, if the price is an integer and > 0 etc) and maps user filters to DB fields.

5. `PlaceService` invokes `find_places_by_filters(filters)` on `PlaceRepository` to query the database

6. `PlaceRepository` executes a database query and returns a list of `Place` objects.

7. (Optional) `PlaceService` calls `get_amenities_for_places(place_ids)` on `AmenityRepository` to enrich results

8. `PlaceService` returns a list of places (with or without amenities) to `PlaceAPI`

9. `PlaceAPI` serialises the result into JSON and returns a `200 OK` HTTP response to the user.


### Alternatives

- If no places are found, the service returns an empty list:
	- API still responds with a `200 OK` status (along with an empty list [])

- If an error occurs (invalid filter) then the API returns a `400 Bad Request` response along with an error message.


### Design Considerations

- This call adheres to RESTful principles using the `GET` request

- The the **Facade Pattern** where `PlaceService` acts as the facade between the API and data.

- The system follows a clean separation between presentation, business logic and data layers where:
   - API handles request/response
  - Service handles logic
  - Repository handles data access
