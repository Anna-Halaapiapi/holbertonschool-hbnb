# Review - Sequence Diagram Documentation
This documentation corresponds with the Review Sequence Diagram, which illustrates the process of creating a review in the HBnB application. 
It shows how the various components interact with each other - to validate data and save a review.

## Overview

When a user submits a review via the API, the application validates the provided `user_id` and `place_id` before saving the review. This ensures that the review is associated with valid and existing entities in the database. 
The Sequence Diagram outlines the interaction between system components, including how validation and error handling is managed. 

## Components
| Actor            | Layer                | Role                                                                                              |
| ---------------- | -------------------- | ------------------------------------------------------------------------------------------------- |
| User             | Client               | Initiates the request via web interface or mobile app                                             |
| ReviewAPI        | Presentation Layer   | Receives and handles POST requests                                                                |
| ReviewService    | Business Logic Layer | Validates input and calls to UserService, PlaceService, ReviewRepository to create/update reviews |
| PlaceService     | Business Logic Layer | Verifies if a place exists and is valid for reviewing. E.g. User had booked it                    |
| UserService      | Business Logic Layer | Verifies that the User ID exists and is valid for the review operation                            |
| PlaceRepository  | Persistence Layer    | Fetches place data from the database                                                              |
| UserRepository   | Persistence Layer    | Fetches user data from database                                                                   |
| ReviewRepository | Persistence Layer    | Saves review to database                                                                          |`

## Flow of Events

1. User sends a `POST` request to the `ReviewAPI` with review data - including `user_id` and `place_id`, rating and comment.

2. The `ReviewAPI` parses and forwards the request to the `ReviewService` to handle the business logic. 

3. The `ReviewService` first calls the `PlaceService` to validate the `place_id`

4. The `PlaceService` fetches the place using the `PlaceRepository`. If the place is found, then the object is returned. Otherwise, an error is raised and a `404` response is returned to the user.

5. Similarly, the `ReviewService` calls the `UserService` to validate the `user_id`. 

6. The `UserService` then queries the `UserRepository` where if the user is found, the object is returned. Otherwise, a `404` response is sent to the user.

7. Once both the `User` and `Place` are validated, the `ReviewService` creates a new review object.

8. The review is then saved to the `ReviewRepository`

9. The saved review is returned to the `ReviewAPI`, which responds with `201 Created` status to the user.

## Alternatives / Error Handling

The diagram includes `alt` fragments to represent the conditional flows:

-  If the Place or User does not exist, then the system exits the normal flow and returns a `404` Error
-  These `alt/else` blocks model the control logic, similar to `if/else` statements in the code.

## Design Considerations

-  Returning the `User` and `Place` objects during validation prevents repeated database lookups and keeps the service layer efficient.
-  This also ensures that the review is created with valid object references - as opposed to just raw IDs
