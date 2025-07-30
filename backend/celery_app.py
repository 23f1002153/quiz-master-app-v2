from celery import Celery
from celery.schedules import crontab

# Create Celery instance
celery = Celery(
    'quiz-master-app',
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    include=['app.tasks']
)

# Define periodic task schedule
# celery.conf.beat_schedule = {
#     'daily-reminder-task': {
#         'task': 'tasks.reminders.send_daily_reminders',
#         'schedule': crontab(hour=19, minute=0),  # You can adjust this for testing
#     },
# }

# Optional: timezone setting
celery.conf.timezone = 'Asia/Kolkata'  # or UTC

# Flask app integration
def make_celery(app):
    celery.conf.update(app.config)
    return celery


