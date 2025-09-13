
# QuizMaster - Exam Preparation Platform

QuizMaster is a full-stack, multi-user application designed to serve as an exam preparation site. It provides a robust platform for students to take quizzes across various subjects and for administrators to manage all aspects of the content and user activity.

## Features

### For Users (Students)
- **Authentication:** Secure user registration and login system.
- **Profile Management:** View and update personal profile information.
- **Browse Content:** Navigate through a structured hierarchy of subjects and their respective chapters.
- **Interactive Quizzing:**
	- Timed quizzes to simulate exam conditions.
	- Start, resume, and submit quizzes.
	- View detailed results and correct answers after quiz completion.
- **Performance Dashboard:** Track personal progress with detailed analytics, including average scores and performance by subject.
- **Quiz History:** A "Quizzeria" section to view all completed quizzes with filtering and sorting capabilities.
- **Data Export:** Trigger an asynchronous job to export personal quiz history to a CSV file, delivered via email.

### For Administrators
- **Admin Dashboard:** A central hub for platform management and analytics.
- **Full CRUD Functionality:**
	- Subjects: Create, read, update, and delete subjects.
	- Chapters: Create, read, update, and delete chapters within subjects.
	- Quizzes: Create, read, update, and delete quizzes, including questions and options.
- **User Management:** View a comprehensive list of all registered users and their details.
- **Platform Analytics:** Access a dashboard with key performance indicators (KPIs) like total users, quiz attempts, and average scores across the entire platform.
- **Data Export:** Trigger an asynchronous job to export performance reports for all users.

### System & Backend
- **Asynchronous Tasks:** Utilizes Celery and Redis for handling long-running background jobs, ensuring the user interface remains responsive.
- **Scheduled Jobs (Celery Beat):**
	- Daily Reminders: Automatically sends email reminders to inactive users about new quizzes.
	- Monthly Reports: Generates and emails a personalized monthly activity report to every user.
- **Caching:** Implements Redis for caching database queries to improve performance and reduce load times.
- **RESTful API:** A well-structured Flask-based API to serve the frontend application.

## Tech Stack

- **Frontend:** Vue.js (with Vue Router for navigation and Pinia for state management)
- **Backend:** Flask (using Flask-RESTful for the API, Flask-SQLAlchemy for the ORM, and Flask-JWT-Extended for authentication)

pip install -r requirements.txt
npm install
npm run dev
**Database:** SQLite
**Caching:** Redis
**Asynchronous Task Queue:** Celery with a Redis broker

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites
- Python 3.x
- Node.js and npm
- Redis Server

### 1. Backend Setup

Navigate to the backend directory:

```sh
cd backend
```

Create and activate a virtual environment:

**For macOS/Linux:**
```sh
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```sh
python -m venv venv
.\venv\Scripts\activate
```

Install the required Python packages:
```sh
pip install -r requirements.txt
```

Create an environment file:
Create a file named `.env` in the backend directory and add the following variables. Replace the placeholder values with your actual credentials.

```env
# A strong, random secret key for JWT
JWT_SECRET_KEY='your-super-secret-jwt-key'

# Your Gmail credentials for sending emails
MAIL_USERNAME='your-email@gmail.com'
MAIL_PASSWORD='your-gmail-app-password'
```

> **Note:** For `MAIL_PASSWORD`, it's highly recommended to use a "Google App Password" instead of your regular Gmail password for better security.

Initialize the database:
This command will create the `database.db` file and create a default admin user (username: admin, password: admin123).

```sh
python create_db.py
```

### 2. Frontend Setup

Navigate to the frontend directory in a new terminal:

```sh
cd frontend
```

Install the required npm packages:
```sh
npm install
```

## Running the Application

You will need to have 5 separate terminals running to launch all the necessary services.

### Start Redis Server
Make sure your Redis server is running. If you installed it locally, you can usually start it with:

```sh
redis-server
```

### Start the Flask Backend Server
(In the backend directory with virtual environment activated)

```sh
python run.py
```

The backend will be available at [http://localhost:5000](http://localhost:5000).

### Start the Vue.js Frontend Server
(In the frontend directory)

```sh
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173) (or another port if 5173 is busy).

### Start the Celery Worker
(In the backend directory with virtual environment activated)
This worker listens for and executes background tasks.

```sh
celery -A celery_worker.celery worker --loglevel=info
```

### Start Celery Beat (Scheduler)
(In the backend directory with virtual environment activated)
This service is responsible for triggering scheduled tasks like daily reminders.

```sh
celery -A celery_worker.celery beat --loglevel=info
```

Now, you can open your browser and navigate to the frontend URL to use the application.