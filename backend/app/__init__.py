from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.config import Config
from app.extensions import db, jwt
from app.api import *
from celery_app import init_celery
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration from the Config object
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Set up the API and register all the routes
    api = Api(app)
    register_auth_routes(api)
    register_user_routes(api)
    register_subject_routes(api)
    register_chapter_routes(api)
    register_quiz_routes(api)
    register_question_routes(api)
    register_option_routes(api)
    register_attempt_routes(api)
    register_job_routes(api)
    
    # Initialize Celery and attach the configured instance to the Flask app object.
    app.celery = init_celery(app)

    return app
