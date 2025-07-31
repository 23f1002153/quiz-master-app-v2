from celery import Celery
from celery.schedules import crontab

# Create and configure the Celery instance in one place.
# This ensures the command-line tool can find the configuration.
celery = Celery(
    'quiz-master-app',
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    include=['app.tasks']
)

# Define the schedule for your periodic tasks (Celery Beat)
celery.conf.beat_schedule = {
    'daily-reminder-task': {
        'task': 'app.tasks.send_daily_reminders',
        'schedule': crontab(hour=19, minute=0),
    },
    'monthly-activity-report': {
        'task': 'app.tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=8, minute=0),
    },
}

# Set the timezone for accurate scheduling
celery.conf.timezone = 'Asia/Kolkata'

# This function is called by the Flask app factory to bind the Celery
# instance to the Flask application context.
def init_celery(app):
    """Binds a Celery instance to the Flask application context."""
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
