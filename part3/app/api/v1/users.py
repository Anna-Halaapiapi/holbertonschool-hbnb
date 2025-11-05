from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


# User-facing endpoints
api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password (will be securely hashed)')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Updated first name'),
    'last_name': fields.String(required=False, description='Updated last name'),
    'email': fields.String(required=False, description='Updated email address'),
    'password': fields.String(required=False, description='Updated password')
})



@api.route('/')
class AdminUserCreate(Resource): 
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    @api.doc(security='jwt') # -- LINE TO BE DELETED AFTER TESTING --
    def post(self):
        """Create a new user - Admin only"""
       
       claims = get_jwt() # Dict containing additional_claims (is_admin)
        is_admin = claims.get('is_admin', False) # defaults to False

        # -- Check admin privileges --
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # -- Check if email is already in use --
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400


        # -- Logic to create a new user -- 
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
    

    @jwt_required()
    @api.doc(security='jwt') # -- LINE TO BE DELETED AFTER TESTING --
    def get(self):
        """Get list of all users - Admin only"""
       
       claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        all_users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in all_users
        ], 200

  

@api.route('/<user_id>')
class AdminUserModify(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.doc(security='jwt') # -- LINE TO BE DELETED AFTER TESTING --
    @jwt_required()
    def get(self, user_id): 
        """Retrieve user details - Admin can view any user / user can view own details"""
       
       claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # -- Allow admins or the user themselves --
        if not is_admin and str(user_id) != str(current_user_id):
            return {'error': 'Unauthorized action.'}, 403

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200


    @api.expect(user_update_model, validate=True) # -- References model so not all fields are required when user updates info --
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input or email already in use')
    @api.response(403, 'Unauthorized action.')
    @api.response(404, 'User not found')
    @api.doc(security='jwt') # -- LINE TO BE DELETED AFTER TESTING --
    @jwt_required()
    def put(self, user_id):
        """Update user details - Admin can modify any user / users can only modify their own"""
        
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        data = request.get_json()
        if not data:
            return {'error': 'Invalid input'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404


        # -- ADMIN LOGIC --

        if is_admin:
            email = data.get('email')
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400


            # -- Logic to update user details --
            try:
                updated_user = facade.update_user(user_id, data)
            except Exception as e:
                return {'error': str(e)}, 400

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200


        # -- REGULAR USER LOGIC --

        if str(user_id) != str(current_user_id):
            return {'error': 'Unauthorized action.'}, 403


        # -- Restrict email and password modification --
        if 'email' in data  or 'password' in data:
            return {'error': 'You cannot modify email or password.'}, 400

        # -- Allow only first name / last name updates --
        update_data = {}
        if 'first_name' in data:
            update_data['first_name'] = data['first_name']
        if 'last_name' in data:
            update_data['last_name'] = data['last_name']


        # -- validate before persisting --
        try:
            updated_user = facade.update_user(user_id, update_data)
        except Exception as e:
            return {'error': str(e)}, 400


        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name
        }, 200
