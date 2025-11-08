from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# facade = HBnBFacade()

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists or invalid input')
    @api.response(403, 'Admin privileges required')
    #@api.doc(security='jwt') # -- USER FOR SWAGGER AUTH. DELETE WHEN TESTING IS COMPLETE --
    @jwt_required()
    def post(self):
        """Create a new amenity - Admin only"""
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        # Create amenity
        data = request.get_json()
        name = data.get('name')


        # -- Check if name is empty --
        if not name:
            return {'error': 'Amenity cannot be empty'}, 400

        # -- Check if amenity name already exists --
        if facade.get_amenity(name):
            return {'error': 'Amenity already exists'}, 400
        
        # -- Create amenity -- 
        try:
            # -- verify that data is valid --
            name = name.strip()
            if not isinstance(name, str) or len(name) == 0:
                return {'error': 'Invalid input: Amenity name cannot be empty'}, 400


            new_amenity = facade.create_amenity(data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.get('id'),
            'name': new_amenity.get('name')
        }, 201
        


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Return a list of all amenities
        # amenities = facade.get_all_amenities()
        # return {"amenities": amenities}, 200
        amenities = facade.get_all_amenities()
        return amenities, 200


@api.route('/<amenity_id>')
class AdminAmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"message": "Amenity not found"}, 404
        return amenity, 200

  
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data or name cannot be empty')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    #@api.doc(security='jwt') # -- USED FOR SWAGGER AUTH. DELETE AFTER TESTING --
    @jwt_required()
    def put(self, amenity_id):
        """Update existing amenity - Admin only"""
        claims = get_jwt()

        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        name = data.get('name')

        # -- Validation for missing 'name' during update --
        if not name:
            return {"error": "A name is required to update an amenity"}, 400

        # -- Retrieve amenity by ID --
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        name = name.strip()
        if not name:
            return {'error': 'Amenity name cannot be empty'}, 400 # -- Ensure name is not empty for update after stripping --

        # -- Verify valid string input for name --
        if not isinstance(name, str) or len(name) == 0:
            return {'error': 'Invalid input: Amenity name must not be empty'}, 400

        # -- Update amenity in database --
        updated_amenity = facade.update_amenity(amenity_id, {"name": name})
        if not updated_amenity:
            return {"error": "Update failed"}, 400

        return {"id": updated_amenity.id, "name": updated_amenity.name}, 200

