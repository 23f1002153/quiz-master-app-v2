


# # Import the celery instance directly from your celery_app.py file
# from celery_app import celery
# from flask_mail import Message
# # DO NOT import 'mail', 'db', or 'current_app' at the top level of this file.

# @celery.task
# def send_test_email(recipient_email: str):
#     """
#     Sends a simple test email asynchronously.
#     """
#     # THE FIX: Import the 'mail' instance INSIDE the function.
#     # This breaks the circular import because this code only runs when a worker
#     # executes the task, at which point the Flask app is fully initialized.
#     from app import mail

#     print(f"Attempting to send email to {recipient_email}...")
#     try:
#         msg = Message(
#             subject="Hello from Celery!",
#             recipients=[recipient_email],
#             body="This is a test email sent from an asynchronous Celery background task."
#         )
#         mail.send(msg)
#         print(f"Successfully sent email to {recipient_email}")
#         return f"Email successfully sent to {recipient_email}."
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         # Re-raise the exception to mark the task as FAILED in Celery
#         raise e

# @celery.task
# def addition(x, y):
#     """A simple test task that adds two numbers."""
#     result = x + y
#     print(f"Executing task: {x} + {y} = {result}")
#     return result

# # You will apply the same pattern to your other tasks.
# # For example, if a task needs the database, you would do:
# # from app.extensions import db
# # inside that specific task function.

