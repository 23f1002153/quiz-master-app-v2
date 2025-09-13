import os
from dotenv import load_dotenv

load_dotenv()
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Your email address
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Your email password or app password
class Config:
    # Base directory for database file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # SQLite configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT secret key
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')  # replace in prod

    # Celery
    celery_broker_url = 'redis://localhost:6379/0'
    celery_result_backend = 'redis://localhost:6379/0'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'shrinidhikumar.2003@gmail.com'
    MAIL_PASSWORD = 'wcyy chsm nzym wuxa'  # use App Password, not your main password
    MAIL_DEFAULT_SENDER = 'shrinidhikumar.2003@gmail.com'

    # --- NEW: Caching Configuration ---
    CACHE_TYPE = 'RedisCache'
    # Use a different database number (e.g., 1) to keep cache separate from Celery
    CACHE_REDIS_URL = 'redis://localhost:6379/1' 
    CACHE_DEFAULT_TIMEOUT = 300 # Default cache expiry in seconds (5 minutes)