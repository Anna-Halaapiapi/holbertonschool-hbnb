from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
#from app.api.v1.reviews import serialize_review
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_cors import CORS, cross_origin

api = Namespace('places', description='Place operations')


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

# -- Non-required fields for updating a place --
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
        review_user = facade.get_user(review.user_id)
        user_name = "Unknown"
        if review_user:
            user_name = f"{review_user.first_name} {review_user.last_name}"
            
        reviews_list.append({
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'user_name': user_name
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
def serialize_review(review):
    """Function serializes review object"""
    user = facade.get_user(review.user_id)
    user_name = "Unknown"
    if user:
        user_name = f"{user.first_name} {user.last_name}"
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user_id,
        'place_id': review.place_id
    }


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    # @api.doc(security='jwt')
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
    # @api.doc(security='jwt') # -- USED FOR TESTING IN SWAGGER. DELETE WHEN TESTING IS COMPLETE --
    @jwt_required()
    def put(self, place_id):
        """Update a place - Admins can override ownership"""

        # -- Get current user info --
        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # -- Get place object --
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # -- Check owner: only owner or admin --
        if not is_admin and place.owner.id != user_id:
            return {'error': 'Unauthorized action'}, 403
            
        # -- Get update data from request --
        data = api.payload

        # -- Merge current place data with new data --
        updated_data = {
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner.id,
            "amenities": [a.id for a in getattr(place, 'amenities', [])]
        }

        updated_data.update(data)

        # convert amenity ID to objects
        if 'amenities' in updated_data:
            amenity_objects = []
            for name_or_id in updated_data['amenities']:
                # Try to get by ID first
                amenity = facade.amenity_repo.get(name_or_id)
                if not amenity:
                    # Try to get by name if ID not found
                    amenity_info = facade.get_amenity_by_name(name_or_id)
                    if not amenity_info:
                        return {'error': f"Amenity '{name_or_id}' not found"}, 400
                    amenity = facade.amenity_repo.get(amenity_info['id'])
                amenity_objects.append(amenity)
            updated_data['amenities'] = amenity_objects
        
        # -- Update place via the facade
        try:
            updated_place = facade.update_place(place.id, updated_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return serialize_place(updated_place), 200

    @jwt_required()
    # @api.doc(security='jwt')
    def delete(self, place_id):
        """ Delete a place - Admin can bypass ownership restrictions"""

        user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        place = facade.get_place(place_id)
        if not place:
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
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [serialize_review(r) for r in reviews], 200

    @api.expect(api.model('Review', {
        'text': fields.String(required=True, description='Text of the review'),
        'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    }))
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self, place_id):
        """Create a new review for a place"""
        user_id = get_jwt_identity()
        data = api.payload
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not data or 'text' not in data or 'rating' not in data:
            return {'error': 'Missing text or rating'}, 400
        
        review_data = {
            'text': data['text'],
            'rating': int(data['rating']),
            'user_id': user_id,
            'place_id': place_id
        }

        try:
            new_review = facade.create_review(review_data)
            if isinstance(new_review, tuple):
                new_review = new_review[0]
            return serialize_review(new_review), 201
        except ValueError as e:
            return {'error': str(e)}, 400