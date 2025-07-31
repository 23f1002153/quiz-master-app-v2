# RUN -> celery -A celery_worker.celery worker --loglevel=info -P solo

# Import the celery instance directly from your celery_app.py file
from celery_app import celery
from flask_mail import Message
from datetime import datetime, timedelta
# from app import db
import csv
import os

# ===================================================================
# Task 5a: Daily Reminders
# ===================================================================

@celery.task
def send_daily_reminders():
    """
    Finds users who have been inactive or have new relevant quizzes
    and sends them a reminder notification.
    
    This task is scheduled to run periodically (e.g., every hour or day).
    """
    # Import necessary components inside the task to ensure app context
    from app import mail, create_app
    from app.models import User, Quiz # Assuming you have these models

    app = create_app()
    with app.app_context():
        print("TASK: Running Daily Reminder Check...")

        # --- 1. Fetch Users Who Need Reminders ---
        # This is a placeholder for your database logic.
        # You would query for users who haven't logged in for a certain period.
        # For example, find users whose 'last_login' is more than 2 days ago.
        two_days_ago = datetime.now() - timedelta(days=2)
        inactive_users = User.query.filter((User.last_login > two_days_ago) & (User.role == 'user')).all()
        
        # For demonstration, we'll use a dummy list of users.
        users_to_remind = [
            {'id': 1, 'username': 'Alex', 'email': '23f1002153@ds.study.iitm.ac.in'},
            {'id': 2, 'username': 'Ben', 'email': 'noob.snipy007@gmail.com'},
        ]
        
        # --- 2. Find New Quizzes ---
        # Find quizzes created in the last 24 hours.
        one_day_ago = datetime.now() - timedelta(days=1)
        new_quizzes = Quiz.query.filter(Quiz.created_at > one_day_ago).all()
        
        # For demonstration, use a dummy list.
        # new_quizzes = [
        #     {'name': 'Advanced Calculus', 'subject': 'Mathematics'},
        #     {'name': 'The Periodic Table', 'subject': 'Science'},
        # ]

        if not inactive_users and not new_quizzes:
            print("No inactive users or new quizzes. No reminders sent.")
            return "No reminders needed."

        # --- 3. Send Reminders ---
        for user in inactive_users:
            # You could add logic here to match new quizzes to a user's interests

            reminder_message_body = (
                f"Hi {user.username},\n\n"
                "Just a friendly reminder from QuizMaster! You have some new quizzes waiting for you:\n\n"
            )
            
            for quiz in new_quizzes:
                reminder_message_body += f"- {quiz.name} ({quiz.chapter.subject.name})\n"
                
            reminder_message_body += "\nCome back and test your knowledge!\n\n- The QuizMaster Team"

            try:
                msg = Message(
                    subject="New Quizzes Await on QuizMaster!",
                    recipients=[user.email],
                    body=reminder_message_body
                )
                mail.send(msg)
                print(f"Reminder sent to {user.email}")
            except Exception as e:
                print(f"Failed to send reminder to {user.email}: {e}")

        return f"Daily reminder task complete. Processed {len(inactive_users)} users."

# ===================================================================
# Task 5b: Monthly Activity Report
# ===================================================================

@celery.task
def generate_monthly_report():
    """
    Generates a personalized monthly activity report for all active users
    and sends it via email.
    
    This task is scheduled to run on the first day of every month.
    """
    # Import necessary components inside the task to ensure app context
    from app import mail, create_app
    from app.models import User, Attempt # Assuming you have these models
    from datetime import datetime, timedelta

    app = create_app()
    with app.app_context():
        print("TASK: Starting Monthly Report Generation...")

        # --- 1. Determine the date range for the previous month ---
        
        # --- Logic for Production (Correct way) ---
        # This correctly finds the first and last day of the previous month.
        today = datetime.now()
        first_day_of_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_of_previous_month = first_day_of_current_month - timedelta(seconds=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        print(f"Generating report for date range: {first_day_of_previous_month.date()} to {last_day_of_previous_month.date()}")

        # --- 2. Fetch all active users ---
        active_users = User.query.filter_by(role = 'user').all()
        
        print(f"Found {len(active_users)} active users to process.")
        # --- 3. For each user, gather stats and send the report ---
        for user in active_users:
            print(f"Processing report for {user.email}...")
            # Query for the user's attempts within the date range
            monthly_attempts = Attempt.query.filter(
                Attempt.user_id == user.id,
                Attempt.attempted_at.between(first_day_of_previous_month, last_day_of_previous_month)
            ).all()
            
            # Skip users with no activity in the month
            if not monthly_attempts:
                print(f"No attempts found for {user.email} in this period. Skipping.")
                continue

            # --- Logic to calculate stats from the attempts ---
            total_percentage = sum(attempt.to_dict()['percentage'] for attempt in monthly_attempts)
            average_score = round(total_percentage / len(monthly_attempts))

            subject_performance = {}
            for attempt in monthly_attempts:
                subject_name = attempt.to_dict()['subject_name']
                if subject_name not in subject_performance:
                    subject_performance[subject_name] = {'total': 0, 'count': 0}
                subject_performance[subject_name]['total'] += attempt.to_dict()['percentage']
                subject_performance[subject_name]['count'] += 1
            
            best_subject_name = max(subject_performance, key=lambda sub: subject_performance[sub]['total'] / subject_performance[sub]['count']) if subject_performance else 'N/A'
            
            highest_score_attempt = max(monthly_attempts, key=lambda attempt: attempt.to_dict()['percentage'])
            highest_score_quiz_str = f"{highest_score_attempt.to_dict()['quiz_name']} ({highest_score_attempt.to_dict()['percentage']}%)"
            
            monthly_stats = {
                'username': user.username,
                'month_name': first_day_of_previous_month.strftime("%B %Y"),
                'quizzes_taken': len(monthly_attempts),
                'average_score': average_score,
                'best_subject': best_subject_name,
                'highest_score_quiz': highest_score_quiz_str
            }

            print(f"Stats for {user.email}: {monthly_stats}")

            if monthly_stats['quizzes_taken'] > 0:
                try:
                    # Generate the HTML for the email body
                    html_body = create_html_report(monthly_stats)
                    
                    msg = Message(
                        subject=f"Your QuizMaster Report for {monthly_stats['month_name']} is Here!",
                        recipients=[user.email],
                        html=html_body
                    )
                    mail.send(msg)
                    print(f"Monthly report sent to {user.email}")
                except Exception as e:
                    print(f"Failed to send report to {user.email}: {e}")

        return f"Monthly report task complete. Processed {len(active_users)} users."

# ===================================================================
# Task 5c.1: User-Triggered CSV Export
# ===================================================================

@celery.task
def export_user_quiz_history(user_id: int):
    """
    Fetches a user's quiz history, saves it to a temporary public file,
    and sends an email with a download link as an alert.
    """
    # Import necessary components inside the task to ensure app context
    from app import mail, create_app, db
    from app.models import User, Attempt, Quiz # Assuming you have these models

    app = create_app()
    with app.app_context():
        print(f"TASK: Starting CSV export for user_id: {user_id}...")

        # --- 1. Fetch User and Their Quiz History ---
        user = User.query.get(user_id)
        if not user:
            return "User not found."
        
        attempts = db.session.query(
            Attempt, Quiz
        ).join(Quiz, Attempt.quiz_id == Quiz.id).filter(
            Attempt.user_id == user_id
        ).order_by(Attempt.attempted_at.desc()).all()

        if not attempts:
            send_notification_email(user.email, "Your Quiz History Export", "You have no quiz history to export.")
            return "No quiz history to export."

        # --- 2. Create and Save the CSV File ---
        # Ensure a directory exists for temporary exports
        export_dir = os.path.join(app.static_folder, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        # Create a unique filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"history_{user_id}_{timestamp}.csv"
        file_path = os.path.join(export_dir, filename)

        try:
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['quiz_id', 'chapter_id', 'date_of_quiz', 'score', 'remarks']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for attempt, quiz in attempts:
                    writer.writerow({
                        'quiz_id': quiz.id,
                        'chapter_id': quiz.chapter_id,
                        'date_of_quiz': quiz.date.strftime("%Y-%m-%d"),
                        'score': attempt.total_score,
                        'remarks': quiz.remarks
                    })
            
            print(f"Successfully created CSV file at {file_path}")

            # --- 3. Send the Alert (Email with Download Link) ---
            # The URL must be the full public URL of your application
            base_url = app.config.get('BASE_URL', 'http://localhost:5000')
            download_link = f"{base_url}/static/exports/{filename}"
            
            email_body = (
                f"Hi {user.username},\n\n"
                "Your requested quiz history export is complete.\n\n"
                f"You can download your file using the link below. The link will be active for 24 hours.\n\n"
                f"{download_link}\n\n"
                "- The QuizMaster Team"
            )
            
            send_notification_email(user.email, "Your Quiz History Export is Ready!", email_body)
            print(f"Alert email sent to {user.email}")

        except Exception as e:
            print(f"An error occurred during CSV export for user {user_id}: {e}")
            raise e

        return f"CSV export and notification sent for user {user_id}."

def send_notification_email(recipient, subject, body):
    """Helper function to send a simple email."""
    from app import mail
    msg = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(msg)

# ===================================================================
# Task 5c.2: Admin-Triggered CSV Export of All Users
# ===================================================================

@celery.task
def export_all_user_performance(admin_email: str):
    """
    Generates a CSV report of all users' performance stats, saves it,
    and emails a download link to the requesting admin.
    """
    from app import mail, create_app, db
    from app.models import User, Attempt

    app = create_app()
    with app.app_context():
        print(f"TASK: Starting all-user performance export for {admin_email}...")

        # --- 1. Fetch all non-admin users ---
        users = User.query.filter_by(role='user').all()
        if not users:
            send_notification_email(admin_email, "User Performance Export", "No user data found to export.")
            return "No users to export."

        # --- 2. Calculate stats for each user ---
        user_stats = []
        for user in users:
            attempts = Attempt.query.filter_by(user_id=user.id).all()
            quizzes_taken = len(attempts)
            if quizzes_taken > 0:
                average_score = round(sum(a.to_dict()['percentage'] for a in attempts) / quizzes_taken)
            else:
                average_score = 0
            
            user_stats.append({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'quizzes_taken': quizzes_taken,
                'average_score': average_score,
                'joining_date': user.joiningDate.strftime("%Y-%m-%d")
            })
        
        # --- 3. Create and Save the CSV File ---
        export_dir = os.path.join(app.static_folder, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"all_user_performance_{timestamp}.csv"
        file_path = os.path.join(export_dir, filename)

        try:
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['user_id', 'username', 'email', 'quizzes_taken', 'average_score', 'joining_date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(user_stats)
            
            print(f"Successfully created all-user CSV at {file_path}")

            # --- 4. Send the Alert (Email with Download Link) ---
            base_url = app.config.get('BASE_URL', 'http://localhost:5000')
            download_link = f"{base_url}/static/exports/{filename}"
            email_body = f"The all-user performance export you requested is complete.\n\nDownload it here:\n{download_link}"
            
            send_notification_email(admin_email, "Your User Performance Export is Ready!", email_body)

        except Exception as e:
            print(f"An error occurred during admin CSV export: {e}")
            raise e

        return f"All-user CSV export and notification sent to {admin_email}."


# def send_notification_email(recipient, subject, body):
#     """Helper function to send a simple email."""
#     from app import mail
#     msg = Message(subject=subject, recipients=[recipient], body=body)
#     mail.send(msg)


# --- Your other tasks can remain below ---
@celery.task
def addition(x, y):
    """A simple test task that adds two numbers."""
    result = x + y
    print(f"Executing task: {x} + {y} = {result}")
    return result

def create_html_report(stats):
    """Creates a styled HTML string for the monthly report email."""
    # This is a simple inline-styled HTML template.
    # For more complex designs, consider using a templating engine like Jinja2.
    return f"""
    <html>
      <head>
        <style>
          body {{ font-family: sans-serif; color: #333; }}
          .container {{ max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 10px; }}
          .header {{ font-size: 24px; font-weight: bold; color: #0d6efd; margin-bottom: 20px; }}
          .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
          .stat-box {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }}
          .stat-label {{ font-size: 14px; color: #6c757d; }}
          .stat-value {{ font-size: 20px; font-weight: bold; }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">Your {stats['month_name']} Report</div>
          <p>Hi {stats['username']}, here's a summary of your activity on QuizMaster last month:</p>
          <div class="stat-grid">
            <div class="stat-box">
              <div class="stat-label">Quizzes Taken</div>
              <div class="stat-value">{stats['quizzes_taken']}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Average Score</div>
              <div class="stat-value">{stats['average_score']}%</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Best Subject</div>
              <div class="stat-value">{stats['best_subject']}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Highest Score</div>
              <div class="stat-value">{stats['highest_score_quiz']}</div>
            </div>
          </div>
          <p style="margin-top: 20px;">Keep up the great work! Visit QuizMaster today to continue your learning journey.</p>
        </div>
      </body>
    </html>
    """


