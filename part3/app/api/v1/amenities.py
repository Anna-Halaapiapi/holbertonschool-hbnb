from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

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
    @api.response(400, 'Invalid input data or amenity already exists')
    @api.resopnse(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity - Admin only"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False): # if not 'is_admin' then False is returned
            return, {'error': 'Admin privileges required'}, 403
        
        # Create amenity
        data = request.get_json()
        if not data or 'name' not in data:
            return {"error": "Invalid input"}, 400

        name = data['name'].strip()
        if not name:
            return {'error': 'Amenity cannot be empty'}, 400

        # Ensure name is unique
        existing = facade.get_amenity_by_name(name)
        if existing:
            return {'error': {'Amenity already exists'}, 400

                    
        new_amenity = facade.create_amenity({'name': name})
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Return a list of all amenities
        # amenities = facade.get_all_amenities()
        # return {"amenities": amenities}, 200
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200



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
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json()

        # -- Validation for missing 'name' during update --
        if not data or 'name' not in data:
            return {"error": "Name attribute is required to update amenity"}, 400 # -- clearer message for missing 'name' --

        # -- Retrieve amenity by ID --
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        name = data['name'].strip()
        if not name:
            return {'error': 'Amenity name cannot be empty'}, 400 # -- Ensure name is not empty for update after stripping --

        # -- Update amenity in database --
        updated_amenity = facade.update_amenity(amenity_id, {"name": data['name']})
        if not updated_amenity:
            return {"error": "Update failed"}, 400

        return {"id": updated_amenity.id, "name": updated_amenity.name}, 200
