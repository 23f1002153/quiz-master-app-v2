from app import db

class AttemptResponse(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    selected_option = db.Column(db.Integer, nullable = False)

    ## Foreign Key
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id', ondelete='CASCADE'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable = False)

    def to_dict(self):
        return {
            "id": self.id,
            "selected_option": self.selected_option,
            "attempt_id": self.attempt_id,
            "question_id": self.question_id
        }