from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
# mail = Mail()
# celery = Celery(__name__)