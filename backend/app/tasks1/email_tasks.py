# app/tasks/email_tasks.py

# from flask_mail import Message
# from app import app, mail, celery

# @celery.task(name="send_email_async")
# def send_email_async(subject, recipients, body):
#     with app.app_context():
#         msg = Message(subject=subject, recipients=recipients, body=body)
#         mail.send(msg)
