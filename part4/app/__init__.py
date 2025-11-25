from flask import Flask
from flask_restx import Api
from app.extensions import bcrypt, jwt, db
from flask_cors import CORS


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)
    
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "your-super-secret-key"

    with app.app_context():

        # -- import modules before creating db --
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity

        # -- create tablles for imported models --
        db.create_all()


    # -- DEV USE ONLY! THIS IS TO ADD JWT AUTHORIZATION BUTTON IN SWAGGER -- 
    #authorizations = {
    #    'jwt': {
    #        'type': 'apiKey',
    #        'in': 'header',
    #        'name': 'Authorization',
    #       'description': "Add 'Bearer ' before your JWT token"
    #   }
    #}

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/',
        # authorizations=authorizations # -- TO DELETE AFTER TESTING --
    )
    # move import block here to avoid circular import
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.amenities import api as amenity_name_space
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register amenity namespace
    api.add_namespace(amenity_name_space, path='/api/v1/amenities')
    # Registered places namespace
    api.add_namespace(places_ns, path="/api/v1/places")
    # Register reviews namespace
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    # Register auth namespace
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
