from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.config import Config
from app.extensions import db, jwt
from app.api.auth import register_auth_routes
from app.api.user import register_user_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Setup RESTful API
    api = Api(app)
    
    # Register the routes
    register_auth_routes(api)
    register_user_routes(api)

    return app
