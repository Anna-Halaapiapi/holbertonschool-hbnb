from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.amenities import api as amenity_name_space
from app.api.v1.reviews import api as reviews_ns
from app.extensions import bcrypt


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    # Register amenity namespace
    api.add_namespace(amenity_name_space, path='/api/v1/amenities')
    # Registered places namespace
    api.add_namespace(places_ns, path="/api/v1/places")
    # Register reviews namespace
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    return app
