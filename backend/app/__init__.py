from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.config import Config
from app.extensions import db, jwt
from app.api import *
from celery_app import make_celery

from flask import jsonify
from werkzeug.exceptions import HTTPException

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)

    register_auth_routes(api)
    register_user_routes(api)
    register_subject_routes(api)
    register_chapter_routes(api)
    register_quiz_routes(api)
    register_question_routes(api)
    register_option_routes(api)
    register_attempt_routes(api)
    # Centralized error handling -> Add before submission
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     if isinstance(e, HTTPException):
    #         return jsonify(message=e.description), e.code

    #     app.logger.error(f"Unhandled Exception: {e}", exc_info=True)
    #     return jsonify(message="Internal Server Error"), 500

    celery = make_celery(app)
    app.celery = celery
    
    return app
