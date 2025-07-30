from flask import current_app
from app.extensions import db
from app.models import User, Quiz  # adjust as per your actual model names
from datetime import datetime, timedelta

from celery_app import celery

@celery.task
def send_daily_reminders():
    with current_app.app_context():

        print("REMINDER SENT")

        now = datetime.utcnow()
        yesterday = now - timedelta(days=1)

        # Find users who didn't log in yesterday (mock logic)
        inactive_users = User.query.filter(User.last_login < yesterday).all()

        # Find new quizzes created in the last 24 hours
        new_quizzes = Quiz.query.filter(Quiz.created_at >= yesterday).all()

        # Mock notification logic
        for user in inactive_users:
            print(f"[Reminder] {user.email} - You haven't visited the site recently!")

        for quiz in new_quizzes:
            print(f"[New Quiz Alert] Quiz '{quiz.title}' was added recently!")
