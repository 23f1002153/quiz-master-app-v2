# This file is the official entry point for the Celery worker.

from app import create_app

# Create the Flask app instance using your factory.
# This ensures that all extensions, including Celery, are initialized.
flask_app = create_app()

# Get the configured Celery instance from the Flask app object.
# The Celery CLI will look for this 'celery' variable.
celery = flask_app.celery
