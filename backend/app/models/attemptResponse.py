from app import db

class AttemptResponse(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    ## Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'CASCADE'), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete = 'CASCADE'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable = False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id', ondelete = 'CASCADE'), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "question_id": self.question_id,
            "option_id": self.option_id
        }