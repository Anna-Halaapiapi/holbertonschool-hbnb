import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db' # Sets the URI for the SQLite database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disables tracking of object modifications.

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
