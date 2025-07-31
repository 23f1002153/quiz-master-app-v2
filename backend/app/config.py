import os

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

    # Gmail SMTP
    # MAIL_SERVER = 'smtp-relay.brevo.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = '93917b001@smtp-brevo.com'
    # MAIL_PASSWORD = 'nLxbRCv2w4X0BHp6'  # use App Password, not your main password
    # MAIL_DEFAULT_SENDER = 'noob.snipy007@gmail.com'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'shrinidhikumar.2003@gmail.com'
    MAIL_PASSWORD = 'wcyy chsm nzym wuxa'  # use App Password, not your main password
    MAIL_DEFAULT_SENDER = 'shrinidhikumar.2003@gmail.com'