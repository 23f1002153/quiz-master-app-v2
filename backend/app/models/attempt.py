from app import db
from datetime import datetime

class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key = True)
    attempted_at = db.Column(db.DateTime, nullable = False, default = datetime.now, index = True)
    score = db.Column(db.Integer, nullable = False)
    total_ques = db.Column(db.Integer, nullable = False)
    correct_ans = db.Column(db.Integer, nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = True)

    ## Foreign Key
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable = False, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = False, index = True)

    ## Relationships
    attempt_responses = db.relationship('AttemptResponse', backref='attempt', lazy=True, cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "attempted_at": self.attempted_at.isoformat(),
            "score": self.score,
            "total_ques": self.total_ques,
            "correct_ans": self.correct_ans,
            "completed": self.completed,
            "quiz_id": self.quiz_id,
            "quiz_name": self.quiz.name,
            "user_id": self.user_id,
            "user_name": self.user.name,
            "responses": [response.to_dict() for response in self.attempt_responses]
        }