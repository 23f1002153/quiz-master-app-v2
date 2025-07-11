from app import db
from datetime import datetime

class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now)

    ## Foreign Key
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable = False)

    ## Relationship
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "subject_id": self.subject_id,
            "subject_name": self.subject.name, ## get subject also
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }