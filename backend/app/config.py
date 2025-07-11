import os

class Config:
    # Base directory for database file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # SQLite configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  # replace in prod
