from app import db
from datetime import datetime, timedelta
from app.utils.formatters import format_time
class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    created_at = db.Column(db.DateTime, default = datetime.now)
    updated_at = db.Column(db.DateTime, onupdate = datetime.now)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.String, nullable = False)
    duration = db.Column(db.Integer,nullable = False) # in minutes
    remarks = db.Column(db.String(500))
    passing = db.Column(db.Integer, nullable = False) 

    ## Foreign Key
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='CASCADE'), nullable = False)

    ## Relationship
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete")
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade="all, delete")
    attempt_responses = db.relationship('AttemptResponse', backref='quiz', lazy=True, cascade='all, delete')


    def to_dict(self, include_internal = False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "time":(self.time) if self.time else None,
            "duration": self.duration,"chapter_id": self.chapter_id,
            "chapter_name": self.chapter.name,  ## get chapter also,
            "subject_name": self.chapter.subject.name,  ## get subject also
            "is_started": self.is_started,
            "is_ongoing": self.is_ongoing,
            "is_ended": self.is_ended,
            "attempts": [attempt.to_dict() for attempt in self.attempts],
        }
        if include_internal: # admin 
            data.update({
                "created_at": self.created_at.isoformat() if self.created_at else None,
                "updated_at": self.updated_at.isoformat() if self.updated_at else None,
                "remarks": self.remarks,
                "passing": self.passing,
            })
        
        return data

    @property
    def is_started(self):
        if not self.date or not self.time:
            return False
        
        start_dt = datetime.combine(self.date, format_time(self.time))
        return datetime.now() >= start_dt

    @property
    def is_ongoing(self):
        if not self.date or not self.time or not self.duration or not self.is_started or not self.is_active:
            return False
        start_dt = datetime.combine(self.date, format_time(self.time))
        end_dt = start_dt + timedelta(minutes=self.duration)
        now = datetime.now()
        return start_dt <= now <= end_dt
    
    @property
    def is_ended(self):
        return self.is_started and not self.is_ongoing
