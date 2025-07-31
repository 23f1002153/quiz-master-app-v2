from app.tasks1.email_tasks import send_email_task

def send_email(subject, recipients, body):
    send_email_task.delay(subject, recipients, body)
