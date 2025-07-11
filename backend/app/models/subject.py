from app import db
from datetime import datetime

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.now)

    ## Relationship
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "chapters": [chapter.to_dict() for chapter in self.chapters]
        }