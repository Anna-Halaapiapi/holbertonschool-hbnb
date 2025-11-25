from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('Review', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=False, description='ID of the user'),
    'place_id': fields.String(required=False, description='ID of the place')
})

# -- Serialization Helper --

def serialize_review(review):
    """Function serializes review object"""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id,
        'place_id': review.place.id
        }

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    # @api.doc(security='jwt') # -- USED FOR SWAGGER TESTING. DELETE WHEN COMPLETED --
    @jwt_required()
    def post(self):
        """Register a new review""" 
        try:
            current_user = get_jwt_identity() # get the id of the auth'd user
            review_data = request.json # get dict of HTTP request data
            place_id = review_data.get('place_id') # get place id from the HTTP request data
            place = facade.get_place(place_id) # get place object by id

            # Check: user doesn't own the place they are trying to review
            if place.owner.id == current_user: # return error if user is owner of place
                return {'error': 'You cannot review your own place.'}, 400

            # Check: user hasn't already reviewed the place
            existing_reviews = facade.get_reviews_by_place(place_id) # get all existing reviews for the place
            for review in existing_reviews: # loop through existing reviwws
                if review.user.id == current_user: # return error if user already reviewed place
                    return {'error': 'You have already reviewed this place.'}, 400

            # logic to create a new review
            review_data['user_id'] = current_user # make user id the current user's id
            new_review, error = facade.create_review(review_data)
            if error:
                return {'error': error}, 400
            return serialize_review(new_review), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [serialize_review(review) for review in reviews], 200  # build and return a list of serialized reviews


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review:
            return serialize_review(review), 200
        return {'error': 'Review not found'}, 404


    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action.')
    # @api.doc(security='jwt') # -- USED FOR TESTING IN SWAGGER. DELETE WHEN TESTING IS COMPLETE --
    @jwt_required()
    def put(self, review_id):
        """Update a review - Admins can override ownership"""

        review_data = request.json # get review data from HTTP request
        current_user = get_jwt_identity() # get current user's id
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id) # get existing review object
        if not review:
            return {'error': 'Review not found'}, 404

        # -- Only allow owner or admin --
        if review.user.id != current_user and not is_admin:
            return {'error': 'Unauthorized action.'}, 403

        # -- Validation: Check if rating is within valid range (1-5) --
        rating = review_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            return {'error': 'Rating must be between 1 and 5'}, 400

        # -- Validation: Ensure text is not empty --
        text = review_data.get('text')
        if not text or not text.strip():
            return {'error': 'Review text cannot be empty'}, 400

        # Update review logic
        updated_review = facade.update_review(review_id, review_data)
        return serialize_review(updated_review), 200


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action.')
    # @api.doc(security='jwt') # -- USED FOR SWAGGER TESTING. DELETE WHEN COMPLETE --
    @jwt_required()
    def delete(self, review_id):
        """Delete review - Admin can bypass ownership"""

        current_user = get_jwt_identity() # get current user's id
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id) # get existing review object by id
        if not review:
            return {'error': 'Review not found'}, 404

        # -- Only allow owner or admin --
        if review.user.id != current_user and not is_admin:
            return {'error': 'Unauthorized action.'}, 403

        # delete review logic
        deleted = facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [serialize_review(review) for review in reviews], 200  # build and return a list of serialized reviews
