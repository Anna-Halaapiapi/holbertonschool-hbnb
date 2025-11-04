from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations') #creates a “group” of endpoints under /users aka everything in this file will be prefix with users in the url

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password (will be securely hashed)')
})

@api.route('/')
class UserList(Resource): 
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required() # Authentication required
    def post(self):
        """Create a new user - Admin only"""
        current_user = get_jwt_identity()

        # Check admin privileges
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user with hashed password
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
    
    def get(self):
        """Get all users"""
        all_users = facade.get_all_users()
        users_list = []
        for user in all_users:
            users_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        return users_list, 200
  

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id): 
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200


    # -- Update model defined for Swagger documentation --
    user_update_model = api.model('UserUpdate', {
        'first_name': fields.String(required=False, description='Updated first name'),
        'last_name': fields.String(required=False, description='Updated last name'),
        'email': fields.String(required=False, description='Updated email address'),
        'password': fields.String(required=False, description='Updated password')
    })

    @api.expect(user_update_model, validate=True) # -- References model so not all fields are required when user updates info --
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(400, 'Email already in use')
    @api.response(400, 'Password cannot be empty')
    @api.response(403, 'Unauthorized action.')
    @api.response(404, 'User not found')
    @api.expect(user_update_model, validate=True)
    @jwt_required() # ensure user is authenticated
    def put(self, user_id):
        """Update user details by ID - Admin can modify any user"""
        current_user = get_jwt_identity() # get current auth'd user's id
        update_data = request.get_json()

        if not update_data:
            return {'error': 'Invalid input'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404


        # -- ADMIN LOGIC --

        # Check Admin privileges
        if current_user.get('is_admin', False): # Check if user is admin. If not 'False' then logic continues.
            
            # Admin can update email
            email = update_data.get('email')

            # Ensure email uniqueness
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400

            # Admin can update password(s)
            password = update_data.get('password')
            # Validate if password is provided
            if password is not None:
                if not isinstance(password, str) or not password.strip():
                    return {'error': 'Password cannot be empty'}, 400
                update_data['password'] = password.strip() # p/w is hashed by the Facade


            # -- Admin can update all other fields --
            if 'first_name' in update_data:
                user.first_name = update_data['first_name']
            if 'last_name' in update_data:
                user.last_name = update_data['last_name']
            if 'email' in update_data:
                user.email = update_data['email']


            # -- validate before persisting --
            try:
                user.validate()
            except ValueError as e:
                return {'error': str(e)}, 400


            updated_user = facade.update_user(user_id, update_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200


        # -- REGULAR USER LOGIC --

        # Check: user_id in URL matches current user's id
        if user_id != current_user: # return error if user is trying to mod another user's data
            return {'error': 'Unauthorized action.'}, 403

        update_data = request.get_json() 
        if not update_data:
            return {'error': 'Invalid input'}, 400

        # Check: prevent user from modding their email or password
        if 'email' in update_data or 'password' in update_data: # if email/password in request, return error
            return {'error': 'You cannot modify email or password.'}, 400

        # Update user first/last name if they exist in the request
        if 'first_name' in update_data:
            user.first_name = update_data['first_name']
        if 'last_name' in update_data:
            user.last_name = update_data['last_name']


        # -- validate before persisting --
        try:
            user.validate()
        except ValueError as e:
            return {'error': str(e)}, 400


        updated_user = facade.update_user(user_id, update_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name
        }, 200
