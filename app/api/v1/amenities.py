from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade


api = Namespace('amenities', description='Amenity operations')
# facade = HBnBFacade()
# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Register a new amenity
        data = request.get_json()
        if not data or "name" not in data:
            return {"message": "Invalid input"}, 400
        new_amenity = facade.create_amenity(data)
        return new_amenity, 201


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Return a list of all amenities
        # amenities = facade.get_all_amenities()
        # return {"amenities": amenities}, 200
        return facade.get_all_amenities()


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404
        return amenity, 200

  
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Update an amenity by ID
        data = request.get_json()
        # if not data or "name" not in data:
            # return {"message": "Invalid input"}, 400
        # updated = facade.update_amenity(amenity_id, data)
        # if not updated:
            # return {"message": "Amenity not found"}, 404
        # return updated, 200
        if not data:
            return {"error": "Invalid input"}, 400
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        if 'name' in data:
            amenity.name = data['name']
        updated_amenity = facade.update_amenity(amenity_id, data)
        return updated_amenity, 200

