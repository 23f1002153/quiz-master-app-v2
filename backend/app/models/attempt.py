from app import db
from datetime import datetime

class Attempt(db.Model):
    __tablename__ = 'attempts'

    id = db.Column(db.Integer, primary_key = True)
    
    attempted_at = db.Column(db.DateTime, nullable = False, default = datetime.now)
    total_marks = db.Column(db.Integer, nullable = False)
    total_score = db.Column(db.Integer, nullable = False)
    total_questions = db.Column(db.Integer, nullable = False)
    total_correct = db.Column(db.Integer, nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = False)


    ## Foreign Key
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable = False, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable = False, index = True)

    def to_dict(self):
        return {
            "id": self.id,
            "attempted_at": self.attempted_at.isoformat(),
            "total_marks": self.total_marks,
            "total_score": self.total_score,
            "total_questions": self.total_questions,
            "total_correct": self.total_correct,
            "percentage": round(self.total_score / self.total_marks * 100),
            "completed": self.completed,
            "duration": self.quiz.duration,
            "quiz_id": self.quiz_id,
            "quiz_name": self.quiz.name,
            "user_id": self.user_id,
            "user_name": self.user.username,
            "chapter_name": self.quiz.chapter.name,
            "subject_name": self.quiz.chapter.subject.name,
            "is_ended": self.quiz.is_ended
        }