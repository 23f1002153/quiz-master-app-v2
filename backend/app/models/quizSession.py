from app import db
from datetime import datetime

class QuizSession(db.Model):
    __tablename__ = 'quizSessions'

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'quiz_id', name='unique_user_quiz_session'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "started_at": self.started_at.isoformat(),
            "user_id": self.user_id,
            "quiz_id": self.quiz_id
        }
