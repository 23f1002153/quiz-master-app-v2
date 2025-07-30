from app import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable = False) # handle validation on frontend
    dob = db.Column(db.Date, nullable = False)
    joiningDate = db.Column(db.Date, nullable = False, default = date.today)
    qualification = db.Column(db.String(120), nullable = False)
    college = db.Column(db.String(120), nullable = False)
    last_login = db.Column(db.DateTime, nullable = False, default = datetime.now)
    phone = db.Column(db.Integer, unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(10), nullable=False, default='user')  # 'admin' or 'user'

    ## Relationship
    attempts = db.relationship('Attempt', backref='user', lazy=True, cascade="all, delete")
    attempt_responses = db.relationship('AttemptResponse', backref='user', lazy=True, cascade='all, delete')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'
    
    def to_dict(self):
         return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "phone": self.phone,
            "dob": self.dob.isoformat(),
            "joiningDate": self.joiningDate.isoformat(),
            "qualification": self.qualification,
            "college": self.college,
            "last_login": self.last_login.isoformat(),
            "role": self.role,
            "attempts": [attempt.to_dict() for attempt in self.attempts] ## get all quiz attempts
        }


