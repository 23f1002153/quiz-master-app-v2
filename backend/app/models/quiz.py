from app import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    is_active = db.Column(db.Boolean, nullable = False, default = True)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now)
    updated_at = db.Column(db.DateTime)
    date_time = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer,nullable = False) # in minutes
    remarks = db.Column(db.String(500))
    passing = db.Column(db.Integer, nullable = False) 

    ## Foreign Key
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='CASCADE'), nullable = False)

    ## Relationship
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete")
    attempts = db.relationship('Attempt', backref='quiz', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "date_time": self.date_time.isoformat() if self.date_time else None,
            "duration": self.duration,
            "remarks": self.remarks,
            "passing": self.passing,
            "chapter_id": self.chapter_id,
            "chapter_name": self.chapter.name,  ## get chapter also
        }
