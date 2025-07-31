from app.utils.mail import send_email

send_email(
    subject="Test Email from Flask",
    recipients=["noob.snipy007@gmail.com"],  # replace with your own email
    body="This is a test email to check Flask-Mail + Gmail App Password setup."
)