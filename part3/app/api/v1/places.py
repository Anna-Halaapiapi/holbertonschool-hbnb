from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.api.v1.reviews import serialize_review
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    #'owner_id': fields.String(required=True, description='ID of the owner'), # --- USE JWT ID INSTEAD --
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# -- Optional fields for updating a place --
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

# -- SERIALIZATION HELPER --

def serialize_place(place):
    """Function serializes place object"""

    amenities_list = []
    if hasattr(place, 'amenities') and place.amenities:
        for amenity in place.amenities:
            amenities_list.append({
                'id': amenity.id,
                'name': amenity.name
            })

    # -- Serialize owner (nested data) --
    owner = {
        'id': place.owner.id,
        'first_name': place.owner.first_name,
        'last_name': place.owner.last_name,
        'email': place.owner.email
    }

    # -- Serialize reviews (nested data) --
    reviews_list = []
    for review in facade.get_reviews_by_place(place.id):
        reviews_list.append({
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id
        })
    

    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': owner, # -- Nested owner data --
        'amenities': amenities_list, # -- Nested amenities data (unchanged) --
        'reviews': reviews_list # -- Nested reviews data (unchanged) --
    }



@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security='jwt')
    @jwt_required() 
    def post(self):
        """Register a new place"""

        user_id = get_jwt_identity()

        try:
            place_data = api.payload
            place_data['owner_id'] = user_id  # -- Use JWT user ID

            if 'amenities' in place_data:
                amenities_input = []
                for item in place_data['amenities']:
                    # -- If it looks like an ID (UUID), skip lookup --
                    if '-' in item:
                        amenities_input.append(item)
                    else:
                        amenity = facade.get_amenity_by_name(item)
                        if not amenity:
                            return {'error': f"Amenity with name '{item}' not found"}, 400
                        amenities_input.append(amenity['id'])
                place_data['amenities'] = amenities_input
            

            # -- Ensure 'reviews' are not passed in payload --
            if 'reviews' in place_data:
                del place_data['reviews']


            new_place = facade.create_place(place_data)
            return serialize_place(new_place), 201
        except ValueError as e:
            return {'error': str(e)}, 400


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""

        try:
            places = facade.get_all_places()
            return [serialize_place(place) for place in places], 200
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class AdminPlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')   
    def get(self, place_id):
        """Get place details by ID """

        try:
            place = facade.get_place(place_id)
            if place is None:
                return {'error': 'Place not found'}, 404
            return serialize_place(place), 200
        except ValueError as e:
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='jwt') # -- USED FOR TESTING IN SWAGGER. DELETE WHEN TESTING IS COMPLETE --
    @jwt_required() # ensure user is authenticated
    def put(self, place_id):
        """Update a place - Admins can bypass ownership restrictions"""

        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        try:
            place = facade.get_place(place_id) # get place object by its ID
        except ValueError:
            return {'error': 'Place not found'}, 404

        # -- ownership check: only admin or owner can update --
        if not is_admin and place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403
            
        data = request.get_json()

        # -- Merge existing data with updated data --

        current_data = {
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner.id,
            "amenities": [a.id for a in getattr(place, 'amenities', [])]
        }
        current_data.update(data)

        try:
            updated_place = facade.update_place(place.id, data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return serialize_place(updated_place), 200

    @jwt_required()
    @api.doc(security='jwt')
    def delete(self, place_id):
        """ Delete a place - Admin can bypass ownership restrictions"""
        
        user_id, is_admin = get_current_user()

        try:
            place = facade.get_place(place_id)
        except ValueError:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.place_repo.delete(place_id)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': f'Place {place_id} deleted successfully'}, 200


@api.route('/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Place not found or has no reviews'}, 404
        return [serialize_review(r) for r in reviews], 200
